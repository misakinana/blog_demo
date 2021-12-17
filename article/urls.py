from django.urls import path
from . import views

app_name = 'article' #设置应用名

urlpatterns = [
    path('article_list/', views.article_list, name = 'article_list'),
    path('article_detail/<int:id>/', views.article_detail, name = 'article_detail'),
    path('article_create/', views.article_create, name='article_create'),
    path('article_update/<int:id>/', views.article_update, name='article_update'),
    path('article_delete/<int:id>/', views.article_delete, name = 'article_delete'),
    path('article_safe_delete/<int:id>/', views.article_safe_delete, name = 'article_safe_delete')
]