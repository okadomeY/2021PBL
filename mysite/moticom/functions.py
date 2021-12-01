import datetime
import calendar
import json
from django.utils import timezone
from dateutil.relativedelta import relativedelta

from .models import Report, Genre, Account, ControlMeasure, Comment, NGWord, KeyWord

#データ抽出日付調整
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

def get_charts_context(context, chart_id, labels_list, data_list, title, data_name='data'):
    added_data = {
        chart_id:{
            'title':title,
            'chart_id':chart_id,
            'label_list':labels_list,
            'data_list':data_list,
            },
        }
            
    context[data_name].update(added_data)
    return context
    

def get_count_chart(context, d, fd):
    #直近１ヶ月投稿数取得
    monthly_day_list, monthly_data_list = monthly_count(d,fd)
    #過去1週間の投稿数取得
    weekly_day_list, weekly_data_list = weekly_count(d)
    #過去1年間の月別投稿数取得
    bymonth_day_list, bymonth_data_list = bymonth_count(d)
    #リストに格納
    label_list = [monthly_day_list, weekly_day_list, bymonth_day_list]
    data_list = [monthly_data_list, weekly_data_list, bymonth_data_list]
    id_list = ["monthly", "weekly", "bymonth"]
    titles_list = ["月間投稿数推移", "過去1週間の投稿数推移", "年間投稿数推移"]
    
    for ids, labels, data, title in zip(id_list, label_list, data_list, titles_list):
        get_charts_context(context, ids, labels, data, title)
    
    return context

def genre_count():
    labels = []
    posts_count = []
    genres = Genre.objects.all()
    for genre in genres:
        labels.append(genre.genre_name)
        posts_count.append(Report.objects.filter(genre_id=genre.id).count())
    return json.dumps(labels), json.dumps(posts_count)

def get_genre_chart(context):
    title = "ジャンル別投稿数"
    ID = "genre"
    get_charts_context(context, ID, *genre_count(), title, "genre_count")
    return context
    
def cm_count():
    labels=[]
    posts_count = []
    cms = ControlMeasure.objects.all()
    for cm in cms:
        labels.append(cm.cm_name)
        posts_count.append(Report.objects.filter(cm_id=cm.id).count())
    labels.append("未割り当て")
    posts_count.append(Report.objects.filter(cm_id__isnull=True).count())
    return json.dumps(labels), json.dumps(posts_count)

def get_cm_chart(context):
    title = "管理策別投稿数"
    ID = "cm"
    get_charts_context(context, ID, *cm_count(), title, "cm_count")
    return context
    
    
def assign_cm(report_text):
    assign_ID = []
    KEY_WORDS=KeyWord.objects.all()
    for kw in KEY_WORDS:
        if report_text.find(kw.key_words) != -1:
            assign_ID.append(kw.cm_id)
    if len(assign_ID)==1:
        return assign_ID[0]
    else:
        assign_dict = {}
        for ID in assign_ID:
            assign_dict[ID] = 0
            KW_list = KEY_WORDS.filter(cm_id=ID).values_list('key_words', flat=True)
            for kw in KW_list:
                if report_text.find(kw) != -1:
                    assign_dict[ID] += 1
        max_ID_list = [i[0] for i in assign_dict.items() if i[1] == max(assign_dict.values())]
        if len(max_ID_list)==1:
            return max_ID_list[0]
