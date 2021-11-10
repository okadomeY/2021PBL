from django.contrib import admin

from .models import Report, Genre, ControlMeasure, Account

admin.site.register(Report)
admin.site.register(Genre)
admin.site.register(ControlMeasure)
admin.site.register(Account)
