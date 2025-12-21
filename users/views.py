from django.shortcuts import render, redirect, resolve_url
from django.urls import reverse_lazy, reverse
from django.contrib import auth
from django.contrib.auth.views import LogoutView
from django.views.generic import FormView
from django.contrib.auth.mixins import LoginRequiredMixin

from .forms import LoginForm, RegistrationForm, EditProfileForm

class LoginView(FormView):
    form_class = LoginForm
    template_name = 'users/Login.html'
    
    def get_success_url(self):
        return self.request.GET.get('continue', reverse_lazy('qa:index'))

    def form_valid(self, form):
        user = auth.authenticate(self.request, **form.cleaned_data)
        
        if user:
            auth.login(self.request, user)
            return redirect(self.get_success_url())
        
        form.add_error(None, "Неправильный логин или пароль")
        return self.form_invalid(form)
    
class RegisterView(FormView):
    form_class = RegistrationForm
    template_name = 'users/Register.html'
    success_url = reverse_lazy('qa:index')

    def form_valid(self, form):
        user = form.save()
        if user:
            auth.login(self.request, user)
        return super().form_valid(form)
    
class ProfileEditView(LoginRequiredMixin, FormView):
    login_url = reverse_lazy('users:login')
    
    form_class = EditProfileForm
    template_name = 'users/Profile.html'
    
    success_url = reverse_lazy('users:profile')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.request.user.is_authenticated:
            kwargs['instance'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

def logout_view(request):
    auth.logout(request)
    previous_page = request.META.get('HTTP_REFERER', 'qa:index')
    return redirect(previous_page)