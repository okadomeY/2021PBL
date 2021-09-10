from django.urls import path
from . import views

app_name = 'moticom'
urlpatterns = [
    path('', views.TopView.as_view(), name='index'),
    path('board', views.BoardView.as_view(), name='board'),
    path('report/', views.ReportView.as_view(), name='report'),
    path('complaints', views.ComplaintsView.as_view(), name='complaints'),
    path('help', views.HelpView.as_view(), name='help'),
    path('admin', views.AdminView.as_view(), name='admin'),
    path('report/SC-03', views.CreateView.as_view(), name='SC-03'),
    path('report/SC-04', views.SceretView.as_view(), name='SC-04'),
    path('report/SC-05', views.CompleteView.as_view(), name='SC-05'),
    path('SC-08/', views.CompleteView.as_view(), name='SC-08')

    ]