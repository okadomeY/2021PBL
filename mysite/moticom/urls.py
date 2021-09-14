from django.urls import path

from . import views

app_name = 'moticom'
urlpatterns = [
    path('', views.TopView.as_view(), name='base'),
    path('index', views.IndexView.as_view(), name='index'),
    path('board', views.BoardView.as_view(), name='board'),
    path('report', views.ReportView.as_view(), name='report'),
    path('genre', views.GenreView.as_view(), name='genre'),
    path('complete', views.CompleteView.as_view(), name='complete'),
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('complaints', views.ComplaintsView.as_view(), name='complaints'),
    path('help', views.HelpView.as_view(), name='help'),
    path('admin', views.AdminView.as_view(), name='admin'),
    ]