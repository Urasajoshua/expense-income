from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView



urlpatterns = [
    path('register',views.RegisterView.as_view(),name='register'),
    path('login',views.LoginView.as_view(),name='login'),
    path('email-verify',views.VerifyEmail.as_view(),name='email-verify'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password-reset/<uidb64>/<token>/',views.PasswordTokenCheckApi.as_view(),name='password-reset-confirm',),
    path('request-password-reset/',views.RequestPasswordResetEmail.as_view(),name='request-password'),
    path('password-reset-complete',views.SetNewPassword.as_view(),name='set-password')
]
