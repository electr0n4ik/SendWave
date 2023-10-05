from django import forms
from django.core.exceptions import ValidationError

from .models import Client


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('full_name', 'email', 'comment')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['full_name'].widget.attrs.update(
            {"class": "form-control", "placeholder": "Write client full name"})
        self.fields['email'].widget.attrs.update(
            {"class": "form-control", "placeholder": "Write client email"})
        self.fields['comment'].widget.attrs.update(
            {"class": "form-control", "placeholder": "Write a comment"})

        for field_name in self.fields:
            self.fields[field_name].label = ""
            self.fields[field_name].help_text = ""

    def clean_email(self):
        email = self.cleaned_data['email']
        if len(email) > 30:
            raise ValidationError("Email can be max 30 symbols")
        if '@' not in email:
            raise ValidationError("It's not possible email without '@'.")
        return email
