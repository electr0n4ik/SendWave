from datetime import datetime, timedelta

from django import forms
from django.core.exceptions import ValidationError

from main.models import Client
from .models import Mailing


class MailingForm(forms.ModelForm):
    """Form for email witch is using bootstrap classes widgets and validating some of the fields"""
    class Meta:
        model = Mailing
        fields = ('subject', 'message', 'send_to_client', 'frequency', 'send_datetime')

        widgets = {
            'send_datetime': forms.DateTimeInput(
                attrs={"class": "form-control", 'type': 'datetime-local'})
        }

    def __init__(self, *args, **kwargs):
        # in CreateView we added user = self.request.user
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            self.fields['send_to_client'].queryset = Client.objects.filter(user=user)

        self.fields['subject'].widget.attrs.update(
            {"class": "form-control", "placeholder": "Write email subject"})
        self.fields['message'].widget.attrs.update(
            {"class": "form-control", "rows": 5, "placeholder": "Write your message"})
        self.fields['frequency'].widget.attrs.update(
            {"class": "form-control"})
        self.fields['send_to_client'].widget.attrs.update(
            {"class": "form-control"})

    def clean_send_datetime(self):
        send_datetime = self.cleaned_data['send_datetime']
        cur_datetime = datetime.now() + timedelta(hours=5)

        if send_datetime < cur_datetime:
            raise ValidationError("You can't send emails in the past.")

        return send_datetime


# class ManagerMailingForm(forms.ModelForm):
#     class Meta:
#         model = Email
#         fields = ['is_active']
#         widgets = {
#             'is_active': forms.CheckboxInput()
#         }
#
#     def __init__(self, *args, **kwargs):
#         kwargs.pop('user', None)
#         super().__init__(*args, **kwargs)
