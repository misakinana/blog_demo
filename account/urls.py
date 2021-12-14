from django.urls import path
from . import views

app_name = 'account' #设置应用名

urlpatterns = [
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('register/', views.account_register, name='user_register')
]