from django.contrib import admin

from .models import Report, User, Genre, ControlMeasure, Comment

admin.site.register(User)
admin.site.register(Report)
admin.site.register(Genre)
admin.site.register(ControlMeasure)
admin.site.register(Comment)