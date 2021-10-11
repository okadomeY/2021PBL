import datetime
import calendar
import json
from django.shortcuts import render
from django.views import generic
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.http import HttpResponse

from .models import Report

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
    queryset = Report.objects.filter(
            created_at__lte=timezone.now()
            ).order_by('-created_at')
    template_name = 'moticom/board.html'
    
#報告画面
class ReportView(generic.TemplateView):
    template_name = 'moticom/report.html'
    
#
class GenreView(generic.TemplateView):
    template_name = 'moticom/genre.html'

#
class CompleteView(generic.TemplateView):
    template_name = 'moticom/complete.html'
    
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
class UserView(generic.TemplateView):
    template_name = 'moticom/user.html'

#
class LayoutView(generic.TemplateView):
    template_name = 'moticom/layout.html'

#
class Genre_ManageView(generic.TemplateView):
    template_name = 'moticom/genre_manage.html'
    
#
class FilterView(generic.TemplateView):
    template_name = 'moticom/filter.html'
    
#
class SortingView(generic.TemplateView):
    template_name = 'moticom/sorting.html'

#
class LinkingView(generic.TemplateView):
    template_name = 'moticom/linking.html'