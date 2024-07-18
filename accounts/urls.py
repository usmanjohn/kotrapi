from django.urls import path, include
from .views import UserRegistrationView, UserDetailView, UserProfileView, ActivateAccountView
from . import views
urlpatterns = [
    
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('user/', UserDetailView.as_view(), name='user_detail'),
    path('profile/', UserProfileView.as_view(), name='current_user_profile'),
    path('profile/<int:pk>/', UserProfileView.as_view(), name='user_profile'),
    path('profilelist/', views.ProfileList.as_view(), name='user_profile_list'),
    path('activate/<uuid:token>/', ActivateAccountView.as_view(), name='activate'),
]
