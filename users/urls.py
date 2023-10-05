from django.urls import path
from django.views.decorators.cache import cache_page

from .apps import UsersConfig
from .views import (UserLoginView,
                    UserLogoutView,
                    UserRegistrationCreateView,
                    user_registration_success,
                    user_verification_view,
                    UserProfileUpdateView)

app_name = UsersConfig.name

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('registration/', UserRegistrationCreateView.as_view(), name='registration'),
    path('registration_success/', cache_page(60)(user_registration_success), name='registration_success'),
    path('verification/<int:pk>/<str:token>/', user_verification_view, name='verification'),
    path('profile/', UserProfileUpdateView.as_view(), name='profile')
]
