from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('generate-token/', views.generate_token, name='generate_token'),
    path('check-token/<uuid:token>/', views.check_token, name='check_token'),
    path('webhook/', views.webhook, name='webhook'),
]