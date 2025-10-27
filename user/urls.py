from django.urls import path
from django.contrib.auth import views as auth_views
from user.views import ProfileView, UserCreateView, UserLoginView, VerifyOTPView, home, userlogout, UserDataUpdateView
urlpatterns = [
    path('', home, name="home"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('login/', UserLoginView.as_view(), name="login"),
    path('logout/', userlogout, name="logout"),
    path('update/',UserDataUpdateView.as_view(), name="update"),
    path('change_password/',auth_views.PasswordChangeView.as_view(template_name = "change_password.html"), name="change_password"),
    # for registration with email verification
    path('registration/', UserCreateView.as_view(), name='registration'),
    path('verify_otp/<int:user_id>/',VerifyOTPView.as_view(), name='verify_otp'),
    # for Password Reset
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),
]
