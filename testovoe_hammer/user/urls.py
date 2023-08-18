"""
URL mappings for the user API.
"""
from django.urls import path
from user import views


app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('login/', views.UserCredentialsView.as_view(), name='login'),
    path('auth_code/', views.UserAuthView.as_view(), name='auth_code'),
]