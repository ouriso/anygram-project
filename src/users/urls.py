from django.urls import path
from django.views.generic.base import RedirectView, TemplateView
from . import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
#     path('login/', views.LoginView.as_view(), name='login'),
#     path('logout/', RedirectView.as_view(pattern_name='index'), name='logout'),
#     path('password_change/', views.PasswordChangeView.as_view(),
#          name='password_change'),
#     path('password_change/done/', TemplateView.as_view(
#          template_name='custom_page.html',
#          extra_context={'message': 'Пароль успешно изменен'}
#     ), name='password_change_done'),
#     path('password_reset/', views.PasswordResetView.as_view(),
#          name='password_reset'),
#     path('password_reset/done/', TemplateView.as_view(
#          template_name='custom_page.html',
#          extra_context={'message': 'Пароль успешно сброшен'}
#     ), name='password_reset_done'),
]
