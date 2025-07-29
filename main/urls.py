from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('contact/', views.contact, name='contact'),
    path('test-email/', views.test_email, name='test_email'),
    path('todo/', views.todo_view, name='todo'),
    path('portfolio/<slug:slug>/', views.portfolio_detail, name='portfolio_detail'),
]
