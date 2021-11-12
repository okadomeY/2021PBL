import datetime
import calendar
import json
from django.shortcuts import render, redirect
from django.views import generic
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.http import HttpResponse, HttpResponseRedirect

from .models import Report, Genre, ControlMeasure, Comment
from .forms import ReportForm, CreatePost, AddGenre, CreativeControlMeasure, CreateComment

#データ抽出日付調整
d = datetime.date.today()
yd = (d - datetime.timedelta(days=1))
fd = d.replace(day=1)
ed = d.replace(day=calendar.monthrange(d.year, d.month)[1])

#各ページ共通部品表示用（ヘッダー・フッター・サイドバー）
class TopView(generic.TemplateView):
    template_name = 'moticom/main.html'

#各ページ内容表示用
#TOP
class IndexView(generic.ListView):
    template_name = 'moticom/index.html'
    context_object_name = 'latest_report_list'
    
    #最新投稿10件の取得
    def get_queryset(self):
        return Report.objects.filter(
            created_at__lte=timezone.now()
            ).order_by('-created_at')[:10]
            
#現行使用版:グラフ用データを取得(要改善/DB側で処理できそう/細部に関しても要改善)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #直近１ヶ月投稿数抽出
        monthly_date_label =[fd + datetime.timedelta(days=i) for i in range(calendar.monthrange(d.year, d.month)[1])]
        monthly_posts_count = []
        
        for i in monthly_date_label:
            monthly_posts_count.append(Report.objects.filter(created_at__date=i).count())
            
        context['monthly_day_list'] = json.dumps([i.strftime("%m/%d") for i in monthly_date_label])
        context['monthly_data_list'] = json.dumps(monthly_posts_count)
        
        
        #過去1週間の投稿数抽出
        weekly_date_label = [d + datetime.timedelta(days=i) for i in range(-6, 1)]
        weekly_posts_count = []
        
        for i in weekly_date_label:
            weekly_posts_count.append(Report.objects.filter(created_at__date=i).count())
        
        context['weekly_day_list'] = json.dumps([i.strftime("%m/%d") for i in weekly_date_label])
        context['weekly_data_list'] = json.dumps(weekly_posts_count)
        
        #過去1年間の月別投稿数抽出（DBのタイムゾーンの設定を行えば__monthでフィルターが使える）←現状でも使用可能だった
        bymonth_date_label =[d + relativedelta(months=i) for i in range(-11, 1)]
        bymonth_posts_count = []
        
        for i in bymonth_date_label:
            bymonth_posts_count.append(Report.objects.filter(created_at__month=i.month).count())
            
        context['bymonth_day_list'] = json.dumps([i.strftime("%y/%m") for i in bymonth_date_label])
        context['bymonth_data_list'] = json.dumps(bymonth_posts_count)
        
        return context


#掲示板
class BoardView(generic.ListView):
    model = Report
    template_name = 'moticom/board.html'
    
    def get_context_data(self):
        context = super().get_context_data()
        context['report_list'] = Report.objects.order_by('-created_at')
        context['genre_list'] = Genre.objects.all()
        return context
    
#ジャンル別表示処理
def genre_display(request):
    context = {
               'report_list':Report.objects.filter(genre_id=request.GET.get('genre_id')).order_by('-created_at'),
               'genre_list':Genre.objects.all(),
               }

    return render(request, 'moticom/board.html', context)
    
#報告画面
class ReportView(generic.FormView):
    template_name = 'moticom/report.html'
    form_class = ReportForm
    
    def post(self, request, *args, **kwargs):
        form = ReportForm(request.POST)
        if form.is_valid():
            request.session['request_text'] = request.POST.get('report_text')
            return redirect('moticom:genre')
        else:
            return render(request, 'moticom/report.html', {'form':form})
    
"""
#テキスト取得
def save_report(request):
    request.session['request_text'] = request.POST.get('report_text')
    if form.is_valid():
        return redirect('moticom:genre')
    
"""

class GenreView(generic.FormView):
    template_name = 'moticom/genre.html'
    model = Genre
    form_class = CreatePost
    
#ユーザーIDの取得と代入の必要あり
def create_post(request):
    if request.method == 'POST':
        if request.POST.get('anonymous'):
            form_contents = {
                'report_text':request.session['request_text'],
                'user_id':'1',#←匿名用ユーザーID"1"を入れる
                'genre_id':request.POST.get('genre_id'),
            }
        else:
            form_contents = {
                'report_text':request.session['request_text'],
                'user_id':'2',#←暫定で"2"で適用中、本来はログインユーザーIDを取る
                'genre_id':request.POST.get('genre_id'),
            }
        form = CreatePost(form_contents)
        if form.is_valid():
            form.save()
            newPost = Report.objects.filter(user_id=2).order_by('-created_at')[0]
        else:
            return redirect('moticom:genre')
            
    context = {
        'report_text':newPost.report_text,
        'genre_id':newPost.genre_id,
    }
        
    return render(request, 'moticom/complete.html', context)

#
class ProfileView(generic.TemplateView):
    template_name = 'moticom/profile.html'

#
class ComplaintsView(generic.TemplateView):
    template_name = 'moticom/complaints.html'
    
#
class HelpView(generic.TemplateView):
    template_name = 'moticom/help.html'
    
#管理者用（別アプリに分ける予定）
#
class AdminView(generic.TemplateView):
    template_name = 'moticom/admin.html'

#
class AnalysisView(generic.TemplateView):
    template_name = 'moticom/analysis.html'

#コメント投稿用
def Admin_BoardView(request):
    queryset = Report.objects.all().order_by('-created_at')
    if request.method == 'POST':
        comment_contents = {
            'comment_text':request.POST.get('comment_text'),
            'report_id':request.POST.get('report_id'),
        }
        print(comment_contents)
        comment = CreateComment(comment_contents)
        if comment.is_valid():
            comment.save()
            
        else:
            return redirect('moticom:admin_board')
    
    else:
        comment = CreateComment()
    
    context = {
        'report_list': queryset,
        'form': comment
    }
    return render(request, 'moticom/admin_board.html', context)

#コメント削除用
def DeleteComment(request):
    if request.method == 'POST':
        Comment.objects.get(id=request.POST.get('comment_id')).delete()
    return redirect('moticom:admin_board')
#
class UserView(generic.TemplateView):
    template_name = 'moticom/user.html'

#
class LayoutView(generic.TemplateView):
    template_name = 'moticom/layout.html'

#
class Genre_ManageView(generic.CreateView):
    template_name = 'moticom/genre_manage.html'
    model = Genre
    form_class = AddGenre
    success_url = 'moticom/genre_manage.html'
    
    def get_context_data(self):
        context = super().get_context_data()
        context['genre_list'] = Genre.objects.all()
        return context
        
def create_genre(request):
    if request.method == 'POST':
        add_genre_name = request.POST.get('genre_name')
        context = {
            'genre_list': Genre.objects.all(),
            'form': AddGenre(),
            'error': "同名のジャンルが既に存在します",
        }
        try:
            Genre.objects.get(genre_name = add_genre_name)
            return render(request, 'moticom/genre_manage.html', context)
        except:
            form_addgenre = {
                'genre_name': add_genre_name,
            }
        form = AddGenre(form_addgenre)
        if form.is_valid():
            form.save()

    return redirect('moticom:genre_manage')
    
def delete_genre(request):
    if request.method == 'POST':
        Genre.objects.get(id=request.POST.get('genre_id')).delete()
    return redirect('moticom:genre_manage')
#
class FilterView(generic.TemplateView):
    template_name = 'moticom/filter.html'
    
#
class SortingView(generic.TemplateView):
    template_name = 'moticom/sorting.html'

#
class LinkingView(generic.TemplateView):
    template_name = 'moticom/linking.html'
    
#
class Cm_CreateView(generic.ListView):
    template_name = 'moticom/cm_create.html'
    model         = ControlMeasure

class CreativeControlMeasureView(generic.CreateView):
    template_name = "moticom/cm_create_forms.html"
    model         = ControlMeasure
    form_class    = CreativeControlMeasure
    success_url   = "/moticom/cm_create" #正しいところに移ったときに修正
    def get_form(self):
        form = super(CreativeControlMeasureView, self).get_form()
        form.fields['cm_name'].label = '管理策名'
        form.fields['cm_contents'].label = '管理策'
        form.fields['genre_id'].label = 'ジャンル'
        return form
#管理策データ修正
class UpdateControlMeasureView(generic.UpdateView):
    template_name = "moticom/cm_update_form.html"
    model         = ControlMeasure
    form_class    = CreativeControlMeasure
    success_url   = "/moticom/cm_create" #正しいところに移ったときに修正
    def get_form(self):
        form = super(UpdateControlMeasureView, self).get_form()
        form.fields['cm_name'].label = '管理策名'
        form.fields['cm_contents'].label = '管理策'
        form.fields['genre_id'].label = 'ジャンル'
        return form
#管理策データ削除
class DeleteControlMeasureView(generic.DeleteView):
    template_name = "moticom/cm_delete_form.html"
    model = ControlMeasure
    success_url = "/moticom/cm_create" #正しいところに移ったときに修正
