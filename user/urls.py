from django.urls import path
from user.views import ProfileView, UserCreateView, UserLoginView, VerifyOTPView, home, userlogout, UserUpdateView, ChangePasswordView
urlpatterns = [
    path('', home, name="home"),
    path('profile/', ProfileView.as_view(), name="profile"),
    path('registration/', UserCreateView.as_view(), name='registration'),
    path('verify_otp/<int:user_id>/',VerifyOTPView.as_view(), name='verify_otp'),
    path('login/', UserLoginView.as_view(), name="login"),
    path('logout/', userlogout, name="logout"),
    path('update/',UserUpdateView.as_view(), name="update"),
    path('change_password/',ChangePasswordView.as_view(), name="change_password"),
]
