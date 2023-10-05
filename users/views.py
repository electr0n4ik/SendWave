from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.views import LoginView, LogoutView

from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm
from .models import User
from .services import generate_verification_token


class UserRegistrationCreateView(CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'registration_form.html'
    success_url = reverse_lazy('user:registration_success')

    def form_valid(self, form):
        new_user = form.save()
        verification_token = generate_verification_token()
        new_user.verification_token = verification_token
        new_user.save()

        verification_url = self.request.build_absolute_uri(
            reverse(
                viewname='user:verification',
                args=[new_user.pk, verification_token])
        )

        send_mail(
            subject='Successful registration on MailerService',
            message=f'Click here to activate your profile {verification_url}.',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[new_user.email])
        return super().form_valid(form)


class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'profile_form.html'
    success_url = reverse_lazy('user:profile')

    def get_object(self, queryset=None):
        return self.request.user


def user_registration_success(request):
    return render(request, template_name='registration_success.html')


def user_verification_view(request, pk, token):
    user = get_object_or_404(User, pk=pk, verification_token=token)
    user.is_active = True
    user.verification_token = None
    user.save()
    return redirect('user:login')


class UserLoginView(LoginView):
    model = User
    form_class = UserLoginForm
    template_name = 'login_form.html'
    success_url = reverse_lazy('home:home')

    def form_valid(self, form):
        user = form.get_user()

        if not user.is_active:
            messages.error(
                self.request,
                message='Your account is not activated. Please check your email.'
            )

        return super().form_valid(form)


class UserLogoutView(LogoutView):
    pass
