from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Contact
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget
import re


def is_only_char(field):

    if re.search(r'\d', field):
        return False

    return True


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'
        widgets = {
            'phone': PhoneNumberInternationalFallbackWidget,
            'message': forms.Textarea,
        }

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['city'].required = False
        self.fields['cinema'].required = False

    def clean(self):
        super(ContactForm, self).clean()

        if not is_only_char(self.cleaned_data['name']):
            error_message = 'Your name can\'t contain numbers!'
            self.add_error('name', error_message)
            raise forms.ValidationError(error_message)

        return self.cleaned_data


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'password1',
            'password2',
        )
        help_texts = {
            'username': None
        }

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError("the given email is already registered")
        return self.cleaned_data['email']

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
