from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from .forms import MailingForm  # , ManagerMailingForm
from .models import Mailing


class MailingListView(LoginRequiredMixin, ListView):
    model = Mailing
    template_name = 'mailing_list.html'
    permission_required = []

    def get_queryset(self):
        """Showing a specific emails according who is the request user"""
        if self.request.user.is_superuser or self.request.user.groups.filter(name='manager').exists():
            return Mailing.objects.all()
        return Mailing.objects.filter(send_from_user=self.request.user)


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing_form.html'
    success_url = reverse_lazy('email:list')

    def get_form_kwargs(self):
        """Sending user id to forms.py, so we can show only clients from this user."""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        """Saving the E-mail with the user id from request"""
        if form.is_valid():
            form.instance.send_from_user = self.request.user
            form.save()
        return super().form_valid(form)


class MailingUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Mailing
    form_class = MailingForm
    template_name = 'mailing_form.html'
    success_url = reverse_lazy('email:list')
    permission_required = []

    def has_permission(self):
        """Giving permissions on specific request users"""
        email = self.get_object()
        if self.request.user == email.send_from_user or self.request.user.groups.filter(name='manager').exists():
            return super().has_permission()

    def get_form_kwargs(self):
        """Sending user id to forms.py, so we can show only clients from this user."""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_form_class(self):
        """Showing a specific form according who is the request user"""
        if self.request.user == self.object.send_from_user:
            return MailingForm
        # elif self.request.user.groups.filter(name='manager').exists():
        #     return ManagerMailingForm


class MailingDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Mailing
    template_name = 'mailing_confirm_delete.html'
    success_url = reverse_lazy('email:list')
    permission_required = []

    def has_permission(self):
        """Giving permissions on specific request users"""
        email = self.get_object()
        if self.request.user == email.send_from_user:
            return super().has_permission()
