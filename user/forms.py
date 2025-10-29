from user.models import CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
class Registration(UserCreationForm):
    first_name = forms.CharField(max_length=200, required=True, )
    email = forms.EmailField(required=True)
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email']
        
class OTPVerifyForm(forms.Form):
    email_otp = forms.CharField(
        max_length=6,
        label="Email OTP",
        widget=forms.TextInput(attrs={'placeholder': 'Enter Email OTP'})
    )
    
class UpdateUserData(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields =['username','first_name', 'last_name', 'email']
        
        
class PasswordChangeForm(PasswordChangeForm):
    class Meta :
        model = User
        fields = '__all__'