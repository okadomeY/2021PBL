from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'moticom'
urlpatterns = [
    path('', views.TopView.as_view(), name='main'),
    path('index', views.IndexView.as_view(), name='index'),

#    chart表示用test
#    path('charts', views.Chart_Sw, name='chart'),

    path('board', views.BoardView.as_view(), name='board'),
    path('genre_display', views.genre_display, name='genre_display'),
    path('report', views.ReportView.as_view(), name='report'),
#    path('save_report', views.save_report, name='save_report'),
    path('genre', views.GenreView.as_view(), name='genre'),
    path('complete', views.create_post, name='complete'),
    path('profile', views.ProfileView.as_view(), name='profile'),
    path('complaints', views.ComplaintsView.as_view(), name='complaints'),
    path('help', views.HelpView.as_view(), name='help'),
    
    #管理者用ページ↓
    path('admin', views.AdminView.as_view(), name='admin'),
    path('analysis', views.AnalysisView.as_view(), name='analysis'),
    path('admin_board', views.Admin_BoardView, name='admin_board'),
    path('delete_comment', views.DeleteComment, name='delete_comment'),
    path('user', views.UserView.as_view(), name='user'),
    path('layout', views.LayoutView.as_view(), name='layout'),
    path('genre_manage', views.Genre_ManageView.as_view(), name='genre_manage'),
    path('add_genre', views.create_genre, name='add_genre'),
    path('delete_genre', views.delete_genre, name='delete_genre'),
    path('filter', views.FilterView.as_view(), name='filter'),
    path('sorting', views.SortingView.as_view(), name='sorting'),
    path('linking', views.LinkingView.as_view(), name='linking'),
    path('cm_create', views.Cm_CreateView.as_view(), name='cm_create'),
    path('create', views.CreativeControlMeasureView.as_view(), name='create'),#正しいところに移ったらcm_createに修正
    path('<int:pk>/update', views.UpdateControlMeasureView.as_view(), name='update'), #正しいところに移ったらcm_updateに修正
    path('<int:pk>/delete', views.DeleteControlMeasureView.as_view(), name='delete'), #正しいところに移ったらcm_deleteに修正
    ]
    
    
#フォーム表示用move_to_genreが上手く行けば不要
#    path('report', views.report_form, name='report'),