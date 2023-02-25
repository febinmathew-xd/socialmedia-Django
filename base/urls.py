from django.urls import path
from . import views



urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('login', views.loginUser, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('settings', views.settings, name='settings'),
    path('upload', views.upload, name='upload'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('like-post/<str:pk>', views.like_post, name='like-post'),
    path('delete-post/<str:pk>', views.deletePost, name='delete-post'),
    path('follow', views.follow, name='follow'),
    path('comment', views.commentPost, name='comment'),
    path('search', views.search, name='search')
]