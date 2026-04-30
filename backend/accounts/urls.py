from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('api/register/', views.RegisterAPIView.as_view(), name='api-register'),
    path('api/me/', views.UserProfileAPIView.as_view(), name='api-profile'),
]