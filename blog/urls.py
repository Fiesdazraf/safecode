from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('new/', views.post_create, name='post_create'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('edit/<slug:slug>/', views.post_edit, name='post_edit'),
    path('delete/<slug:slug>/', views.post_delete, name='post_delete'),
    path('comment/delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),
]
