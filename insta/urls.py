from django.urls import path, re_path
from . import views
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from .models import UserModel

app_name = 'insta'
urlpatterns = [
	path('',views.index, name='index'),
	path('login/', views.login_view, name='login'),
	path('signup/', views.signup,  name='signup'),
	path('logout/', views.logout_view, name='logout'),
	path('profile/<int:uid>/', views.profile, name='profile'),
	path('upload_post/', views.upload, name='upload'),
	path('upload_post_no_view/', views.upload_no_view, name='upload_no_view'),
	path('follow/', views.follow, name='follow'),
	path('feed/', views.feed, name='feed'),
	path('edit/', views.edit, name='edit'),
	path('edit_no_view/', views.edit_no_view, name='edit_no_view'),
	path('visit_profile/<int:uid>/<int:visit_uid>/', views.visit_profile, name='visit_profile'),
	path('profile/<int:uid>/<int:post_id>', views.liking_disliking, name='like_dislike'),
	path('report/', views.report, name='report'),
]

"""path('signup/', views.UserCreateView.as_view(), name='signup'),
	path('login/', views.login, name='login'),
	path('logout/', LogoutView.as_view(template_name='insta/logout.html'), name='logout'),
	#path('login/', LoginView.as_view(template_name='insta/select.html'), name='login'),
	re_path(r'/(?P<user_name>.+)/', views.profile, name='profile'),
	re_path(r'(?P<user_name>.+)/followers', views.followers, name='followers'),
	re_path(r'(?P<user_name>.+)/following', views.following, name='following'),
	#re_path(r'^(?P<album_id>[0-9]+)/favorite/$', views.favorite, name='favorite'),success_url=reverse_lazy('login')"""
