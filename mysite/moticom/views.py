import datetime
import calendar
import json
from django.shortcuts import render, redirect
from django.views import generic
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy, reverse

from .models import Report, Genre, Account
from .forms import ReportForm, CreatePost, AddGenre, SearchForm, MyPasswordChangeForm#LoginForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView,PasswordChangeView, PasswordChangeDoneView

from django.views.generic.edit import CreateView

from django.contrib.auth.decorators import login_required

from .forms import AccountForm#, AddAccountForm # ユーザーアカウントフォーム

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.mixins import LoginRequiredMixin



#データ抽出日付調整
d = datetime.date.today()
yd = (d - datetime.timedelta(days=1))
fd = d.replace(day=1)
ed = d.replace(day=calendar.monthrange(d.year, d.month)[1])

#各ページ共通部品表示用（ヘッダー・フッター・サイドバー）
class TopView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'moticom/main.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs) # 継承元のメソッドCALL
        context["form_name"] = "main"
        return context

#各ページ内容表示用
#TOP
class IndexView(generic.ListView):
    template_name = 'moticom/index.html'
    #テスト用※完作業了後要削除
#    template_name = 'moticom/index.1.html'
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

"""
#グラフ切り替えテスト版
def Chart_Sw(request):
    if request.method == 'GET':
        if 'monthly' in request.GET:
            monthly_date_label =[fd + datetime.timedelta(days=i) for i in range(calendar.monthrange(d.year, d.month)[1])]
            monthly_posts_count = []
        
            for i in monthly_date_label:
                monthly_posts_count.append(Report.objects.filter(created_at__date=i).count())
                
            day_list = json.dumps([i.strftime("%m/%d") for i in monthly_date_label])
            data_list = json.dumps(monthly_posts_count)
            
        elif 'weekly' in request.GET:
            weekly_date_label = [d + datetime.timedelta(days=i) for i in range(-6, 1)]
            weekly_posts_count = []
        
            for i in weekly_date_label:
                weekly_posts_count.append(Report.objects.filter(created_at__date=i).count())
                    
            day_list = json.dumps([i.strftime("%m/%d") for i in weekly_date_label])
            data_list = json.dumps(weekly_posts_count)
            
        elif 'yearly' in request.GET:
            bymonth_date_label =[d + relativedelta(months=i) for i in range(-11, 1)]
            bymonth_posts_count = []
            
            for i in bymonth_date_label:
                bymonth_posts_count.append(Report.objects.filter(created_at__month=i.month).count())
                
            day_list = json.dumps([i.strftime("%y/%m") for i in bymonth_date_label])
            data_list = json.dumps(bymonth_posts_count)
        
        data_set = {
            'day_list': day_list,
            'data_list': data_list,
        }
        return HttpResponse(data_set)
"""

#掲示板
class BoardView(generic.ListView):
    context_object_name = 'latest_report_list'
    queryset = Report.objects.filter(
            created_at__lte=timezone.now()
            ).order_by('-created_at')
    template_name = 'moticom/board.html'
    
#報告画面
class ReportView(generic.TemplateView):
#    template_name = 'moticom/report.html'
    template_name = 'moticom/report_copy.html'
    form_class = ReportForm
    
    
    
#要追加→テキストが空白の場合の処理
def save_report(request):
    request.session['request_text'] = request.POST.get('report_text')
    return redirect('moticom:genre')
        
        
#
class GenreView(generic.TemplateView):
    template_name = 'moticom/genre.html'
    model = Genre
    form_class = CreatePost
    

#ユーザーIDの取得と代入の必要あり
def create_post(request):
    if request.method == 'POST':
        form_contents = {
            'report_text':request.session['request_text'],
            'user_id':'1',#←暫定で"1"で適用中
            'genre_id':request.POST.get('genre_id'),
        }
        form = CreatePost(form_contents)
        if form.is_valid():
            form.save()
            newPost = Report.objects.filter(user_id=1).order_by('-created_at')[0]
        else:
            return redirect('moticom:genre')
            
    context = {
        'report_text':newPost.report_text,
        'genre_id':newPost.genre_id,
    }
        
    return render(request, 'moticom/complete.html', context)

#
#class CompleteView(generic.TemplateView):
#    template_name = 'moticom/complete.html'
    
#
class ProfileView(generic.TemplateView):
    template_name = 'moticom/profile.html'

#
class ComplaintsView(generic.TemplateView):
    template_name = 'moticom/complaints.html'
    
#
class HelpView(generic.TemplateView):
    template_name = 'moticom/help.html'
    
#
class AdminView(generic.TemplateView):
    template_name = 'moticom/admin.html'

#
class AnalysisView(generic.TemplateView):
    template_name = 'moticom/analysis.html'

#
#class UserView(generic.TemplateView):
#      template_name = 'moticom/user.html'

#def user(request):
#    user_list = Account.objects.all()
#    params = {'user_list':user_list}
#    return render(request, 'moticom/user.html', params)

class UserView(ListView):
    template_name = 'moticom/user.html'
    model = Account
    context_object_name = 'user_list'

#
class LayoutView(generic.TemplateView):
    template_name = 'moticom/layout.html'

#
class Genre_ManageView(generic.TemplateView):
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
        form_addgenre = {
            'genre_name':request.POST.get('genre_name'),
        }
        form = AddGenre(form_addgenre)
        if form.is_valid():
            form.save()

    return redirect('moticom:genre_manage')
    
#
class FilterView(generic.TemplateView):
    template_name = 'moticom/filter.html'
    
#
def sorting(request):
    report_list = Report.objects.all()
    params = {'report_list':report_list}
    return render(request, 'moticom/sorting.html', params)

#
class LinkingView(generic.TemplateView):
    template_name = 'moticom/linking.html'
    
def Search(request):
    if request.method == 'POST':
        searchform = SearchForm(request.POST)
        
        if searchform.is_valid():
            freeword = searchform.cleaned_data['freeword']
            search_list = Report.objects.filter(Q(user_id__user_name__icontains = freeword)|Q(genre_id__genre_name__icontains = freeword)|Q(report_text__icontains = freeword))
            
        params = {
            'search_list':search_list,
        }
        
        return render(request, 'moticom/search.html', params)


#class Login(LoginView):
#    form_class = LoginForm
#    template_name = 'moticom/login.html'
#    
#@login_required
class Logout(LogoutView):
    template_name = 'moticom/logout.html'

#class SignUp(CreateView):
#    form_class = SignUpForm
#    template_name = "moticom/signup.html" 
#    success_url = reverse_lazy('moticom:user')
#
#    def form_valid(self, form):
#        user = form.save() # formの情報を保存
#        login(self.request, user) # 認証
#        self.object = user 
#        return HttpResponseRedirect(self.get_success_url()) # リダイレクト
        
        
#ログイン
def Login(request):
    # POST
    if request.method == 'POST':
        # フォーム入力のユーザーID・パスワード取得
        ID = request.POST.get('username')
        Pass = request.POST.get('password')

        # Djangoの認証機能
        user = authenticate(username=ID, password=Pass)

        # ユーザー認証
        if user:
            #ユーザーアクティベート判定
            if user.is_active:
                # ログイン
                login(request,user)
                # ホームページ遷移
                return HttpResponseRedirect(reverse('moticom:main'))
            else:
                # アカウント利用不可
                return HttpResponse("アカウントが有効ではありません")
        # ユーザー認証失敗
        else:
            return HttpResponse("ログインIDまたはパスワードが間違っています")
    # GET
    else:
        return render(request, 'moticom/login.html')

#ログアウト
#@login_required
#def Logout(request):
#    logout(request)
#    # ログイン画面遷移
#    return HttpResponseRedirect(reverse('login'))


class  SignUp(generic.TemplateView):

    def __init__(self):
        self.params = {
        "AccountCreate":False,
        "account_form": AccountForm(),
        #"add_account_form":AddAccountForm(),
        }

    # Get処理
    def get(self,request):
        self.params["account_form"] = AccountForm()
        #self.params["add_account_form"] = AddAccountForm()
        self.params["AccountCreate"] = False
        return render(request,"moticom/signup.html",context=self.params)

    # Post処理
    def post(self,request):
        self.params["account_form"] = AccountForm(data=request.POST)
        #self.params["add_account_form"] = AddAccountForm(data=request.POST)

        # フォーム入力の有効検証
        if self.params["account_form"].is_valid(): #and self.params["add_account_form"].is_valid():
            # アカウント情報をDB保存
            account = self.params["account_form"].save()
            # パスワードをハッシュ化
            #account.set_password(account.password)
            # ハッシュ化パスワード更新
            account.save()

            # 下記追加情報
            # 下記操作のため、コミットなし
            #add_account = self.params["add_account_form"].save(commit=False)
            #AccountForm & AddAccountForm 1vs1 紐付け
            #add_account.user = account

            # モデル保存
            #add_account.save()

            # アカウント作成情報更新
            self.params["AccountCreate"] = True

        else:
            # フォームが有効でない場合
            print(self.params["account_form"].errors)

        return render(request,"moticom/signup.html",context=self.params)
        

#class PasswordChange(LoginRequiredMixin, PasswordChangeView):
#    """パスワード変更ビュー"""
#    success_url = reverse_lazy('moticom:password_change_done')
#    template_name = 'moticom/password_change.html'

#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs) # 継承元のメソッドCALL
#        context["form_name"] = "password_change"
#        return context

#class PasswordChangeDone(LoginRequiredMixin,PasswordChangeDoneView):
#    """パスワード変更完了"""
#    template_name = 'moticom/password_change_done.html'

class PasswordChange(PasswordChangeView):
    """パスワード変更ビュー"""
    form_class = MyPasswordChangeForm
    success_url = reverse_lazy('moticom:password_change_done')
    template_name = 'moticom/password_change.html'


class PasswordChangeDone(PasswordChangeDoneView):
    """パスワード変更しました"""
    template_name = 'moticom/password_change_done.html'