from django import forms
from django.forms import ModelForm
from django.shortcuts import render

from newsletter.models import SubscribedUser


class NewsletterRegistrationForm(ModelForm):

    class Meta:
        model = SubscribedUser
        fields = '__all__'

    def clean(self):
        cleaned_data = self.cleaned_data
        request_email = cleaned_data['email']

        if request_email and SubscribedUser.objects.filter(email=request_email):
            error_message = 'You are already subscribed to our newsletter!'
            self.add_error('email', error_message)
            raise forms.ValidationError(error_message)

        return cleaned_data
