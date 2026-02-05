from django.urls import include, path

from . import views

urlpatterns=[
    path('', views.home, name='index'),
    path('signup/', views.signUp, name='signup'),
    path('signin/', views.signIn, name='signin'),
    path('logout/', views.logOut, name='logout'),
    path('settings/<int:pk>/', views.settings, name='settings'),
    path('upload/<int:pk>/', views.upload, name='upload'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('likepost/', views.likepost, name='likepost'),
    path('follow/', views.follow, name='follow'),
]