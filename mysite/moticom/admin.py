from django.contrib import admin

from .models import Report, User, Genre, ControlMeasure, Comment, Account, KeyWord

admin.site.register(Report)
admin.site.register(Genre)
admin.site.register(ControlMeasure)
admin.site.register(Comment)
admin.site.register(Account)
admin.site.register(KeyWord)