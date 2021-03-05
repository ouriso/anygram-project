from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('password_change/', views.PasswordChangeView.as_view(),
         name='password_change'),
    path('password_reset/', views.PasswordResetView.as_view(),
         name='password_reset'),
]
