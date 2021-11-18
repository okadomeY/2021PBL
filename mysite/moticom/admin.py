from django.contrib import admin

<<<<<<< HEAD
from .models import Report, User, Genre, ControlMeasure, Comment
=======
from .models import Report, Genre, ControlMeasure, Account
>>>>>>> e083bf5f4462247b5f994f65cd34c400cf2d1451

admin.site.register(Report)
admin.site.register(Genre)
admin.site.register(ControlMeasure)
<<<<<<< HEAD
admin.site.register(Comment)
=======
admin.site.register(Account)
>>>>>>> e083bf5f4462247b5f994f65cd34c400cf2d1451
