import datetime
import calendar
import json
from django.utils import timezone
from dateutil.relativedelta import relativedelta

from .models import Report, Genre, Account, ControlMeasure, Comment, NGWord

#チャート表示用
#投稿数取得関数
def get_charts_count(date_label):
    posts_count = []
    
    for i in date_label:
        posts_count.append(Report.objects.filter(created_at__date=i).count())
    
    return json.dumps(posts_count)