from django.shortcuts import render, redirect, get_object_or_404
from user.forms import Registration,OTPVerifyForm, UpdateUserData, PasswordChangeForm
from django.views.generic import CreateView, FormView, UpdateView, DetailView
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from user.models import CustomUser
from django.core.mail import send_mail
from django.conf import settings
from user.utils import generate_otp, verify_otp
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
# Create your views here.
@login_required
def profile(request):
    return render(request, 'profile.html')
def home(request):
    return render(request, 'home.html')
def userlogout(request):
    logout(request)
    messages.success(request, "Logged Out !")
    return redirect('login')


class UserCreateView(FormView):
    form_class = Registration
    template_name = "registration.html"
    

    def form_valid(self, form):
        user = CustomUser.objects.create_user(
            username=form.cleaned_data['username'],
            email= form.cleaned_data['email'],
            password= form.cleaned_data['password1']
        )
        user.is_active = False
        email_otp = generate_otp()
        user.email_otp = email_otp
        self.request.session['pending_user'] = form.cleaned_data
        user.save()
        send_mail(
            'Email Verification OTP',
            f'Your OTP for email verification is: {email_otp}',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )

        return redirect('verify_otp', user_id=user.id)
    
    def form_invalid(self, form):
        messages.error(self.request, "Please Enter Valid Data")
        return super().form_invalid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Registration'
        return context


class VerifyOTPView(FormView):
    template_name = 'verify_otp.html'
    form_class = OTPVerifyForm
    # success_url = reverse_lazy('profile')

    def dispatch(self, request, *args, **kwargs):
        self.user = get_object_or_404(CustomUser, id=kwargs['user_id'])
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        email_otp = form.cleaned_data['email_otp']
        form_data = self.request.session.get('pending_user')
        if verify_otp(email_otp, self.user.email_otp):
            self.user.is_email_verified = True
            self.user.email_otp = None
            self.user.is_active = True  
            self.user.save()
            login(self.request, self.user)
            messages.success(self.request, "OTP verified successfully!")
            return redirect('profile')

        messages.error(self.request, "Invalid OTP")
        return self.form_invalid(form)
    
class UserLoginView(LoginView):
    template_name = "registration.html"
    def get_success_url(self):
        return reverse_lazy("profile")
    
    def form_valid(self, form):
        messages.success(self.request, "Successfully Loged In")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request, "Plese enter Valid Information")
        return super().form_invalid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = "Login" 
        return context
    
@method_decorator(login_required,name='dispatch')
class UserDataUpdateView(UpdateView):
    model = User
    form_class = UpdateUserData
    template_name = 'registration.html'
    success_url = reverse_lazy('profile')
    def form_valid(self, form):
        messages.success(self.request, "Successfully Updated User Data")
        form.save()
        return super().form_valid(form)
    def get_object(self, queryset = None):
        return self.request.user
    def form_invalid(self, form):
        messages.error(self.request, "Sorry User Data Not Updated")
        return super().form_invalid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["type"] = "Update Profile" 
        return context
# @method_decorator(login_required,name='dispatch')    
# class ChangePasswordView(FormView):
#     form_class = PasswordChangeForm
#     template_name = "registration.html"
#     success_url = reverse_lazy('profile')
    
#     def get_form_kwargs(self):
#         kargs = super().get_form_kwargs()
#         kargs['user'] = self.request.user
#         return kargs
#     def form_valid(self, form):
#         form.save()
#         messages.success(self.request, "Successfully Updated Password")
#         return super().form_valid(form)
#     def form_invalid(self, form):
#         messages.error(self.request, "Plese enter Valid Information")
#         return super().form_invalid(form)
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["type"] = "Password" 
#         return context
    
    

    
        
    
    
