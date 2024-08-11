from django.urls import path
from django.contrib.auth import views as auth_views
from .views import article_list, article_detail, article_create, about, privacy, register, login_view, logout_view

urlpatterns = [
    path('', article_list, name='article_list'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register, name='register'),
    path('about/', about, name='about'),
    path('privacy/', privacy, name='privacy'),
    path('article/<int:pk>/', article_detail, name='article_detail'),
    path('article/create/', article_create, name='article_create'),
]

