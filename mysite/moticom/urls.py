from django.urls import path

from . import views

from django.contrib.auth import views as auth_views

app_name = 'moticom'
urlpatterns = [
    path('', views.TopView.as_view(), name='main'),
    path('index', views.IndexView.as_view(), name='index'),

#    chart表示用test
#    path('charts', views.Chart_Sw, name='chart'),

    path('board', views.BoardView.as_view(), name='board'),
<<<<<<< HEAD
    path('genre_display', views.genre_display, name='genre_display'),
=======

#フォーム表示の為一時除外（現在：解除中）
>>>>>>> e083bf5f4462247b5f994f65cd34c400cf2d1451
    path('report', views.ReportView.as_view(), name='report'),

#move_to_genreでは後続の処理に対応できなかったため、削除予定
#    path('genre', views.move_to_genre, name='genre'),

    path('save_report', views.save_report, name='save_report'),

#save_reportのテストのためコメントアウト中
#    path('genre', views.GenreView.as_view(), name='genre'),
    path('genre', views.GenreView.as_view(), name='genre'),
<<<<<<< HEAD
=======

#create_postのテストのためコメントアウト中
#    path('complete', views.CompleteView.as_view(), name='complete'),
>>>>>>> e083bf5f4462247b5f994f65cd34c400cf2d1451
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
    #path('user', views.user, name='user'),
    path('layout', views.LayoutView.as_view(), name='layout'),
    path('genre_manage', views.Genre_ManageView.as_view(), name='genre_manage'),
    path('add_genre', views.create_genre, name='add_genre'),
<<<<<<< HEAD
    path('delete_genre', views.delete_genre, name='delete_genre'),
    path('filter', views.FilterView.as_view(), name='filter'),
    path('delete_NGword', views.delete_NGword, name='delete_NGword'),
    path('sorting', views.SortingView.as_view(), name='sorting'),
    path('linking', views.LinkingView.as_view(), name='linking'),
    path('cm_create', views.Cm_CreateView.as_view(), name='cm_create'),
    path('create', views.CreativeControlMeasureView.as_view(), name='create'),#正しいところに移ったらcm_createに修正
    path('<int:pk>/update', views.UpdateControlMeasureView.as_view(), name='update'), #正しいところに移ったらcm_updateに修正
    path('<int:pk>/delete', views.DeleteControlMeasureView.as_view(), name='delete'), #正しいところに移ったらcm_deleteに修正
    ]
=======
    path('filter', views.FilterView.as_view(), name='filter'),
    path('sorting', views.sorting, name='sorting'),
    path('linking', views.LinkingView.as_view(), name='linking'),
    path('search', views.Search, name='search'),
    #path('sorting', views.SortingView.as_view(), name='sorting'),
    path('login/', views.Login, name='login'),
    path('logout', views.Logout.as_view(), name='logout'),
    path('signup', views.SignUp.as_view(), name='signup'),
    #path('password_change', views.PasswordChange.as_view(), name='password_change'), #パスワード変更
    #path('password_change/done', views.PasswordChangeDone.as_view(), name='password_change_done'), #パスワード完了
    path('password_change/', views.PasswordChange.as_view(), name='password_change'),
    path('password_change/done/', views.PasswordChangeDone.as_view(), name='password_change_done'),
    #path('change_password/', auth_views.PasswordChangeView.as_view(template_name='moticom/password_change.html', success_url = '/'),name='password_change'),
   
    ]

#フォーム表示用move_to_genreが上手く行けば不要
#    path('report', views.report_form, name='report'),
>>>>>>> e083bf5f4462247b5f994f65cd34c400cf2d1451
