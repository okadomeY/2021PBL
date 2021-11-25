import datetime
import calendar
import json
from django.utils import timezone
from dateutil.relativedelta import relativedelta

from .models import Report, Genre, Account, ControlMeasure, Comment, NGWord

#データ抽出日付調整 ←一応コピペ（基本的に不要になる予定）
#d = datetime.date.today()
#yd = (d - datetime.timedelta(days=1))
#fd = d.replace(day=1)
#ed = d.replace(day=calendar.monthrange(d.year, d.month)[1])

#チャート表示用
#投稿数取得関数
def get_count(date_label):
    posts_count = []
    
    for i in date_label:
        posts_count.append(Report.objects.filter(created_at__date=i).count())
    
    return json.dumps(posts_count)
    
#月別投稿数取得関数
def monthly_count(d,fd):
    monthly_date_label =[fd + datetime.timedelta(days=i) for i in range(calendar.monthrange(d.year, d.month)[1])]
    return json.dumps([i.strftime("%m/%d") for i in monthly_date_label]), get_count(monthly_date_label)

#過去1週間の投稿数取得関数
def weekly_count(d):
    weekly_date_label = [d + datetime.timedelta(days=i) for i in range(-6, 1)]
    return json.dumps([i.strftime("%m/%d") for i in weekly_date_label]), get_count(weekly_date_label)

#過去1年間の月別投稿数取得関数
def bymonth_count(d):
    bymonth_date_label =[d + relativedelta(months=i) for i in range(-11, 1)]
    return json.dumps([i.strftime("%y/%m") for i in bymonth_date_label]), get_count(bymonth_date_label)

def get_count_chart(context, d, fd):
    
    #直近１ヶ月投稿数取得
    monthly_day_list, monthly_data_list = monthly_count(d,fd)
    
    #過去1週間の投稿数取得
    weekly_day_list, weekly_data_list = weekly_count(d)
    
    #過去1年間の月別投稿数取得
    bymonth_day_list, bymonth_data_list = bymonth_count(d)
    
    context['data'] = {
                     'monthly':{
                              'chart_id': "monthly",
                              'day_list': monthly_day_list,
                              'data_list': monthly_data_list,
                              },
                              
                     'weekly':{
                             'chart_id': "weekly",
                             'day_list': weekly_day_list,
                             'data_list': weekly_data_list,
                             },
                             
                    'bymonth':{
                             'chart_id': "bymonth",
                             'day_list': bymonth_day_list,
                             'data_list': bymonth_data_list,
                             },
                      }
                      
    return context


