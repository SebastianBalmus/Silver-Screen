from curses.ascii import isalpha
from django import forms
from .models import Contact
from phonenumber_field.widgets import PhoneNumberInternationalFallbackWidget


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

        if not isalpha(self.cleaned_data['name']):
            error_message = 'Your name can\'t contain numbers!'
            self.add_error('name', error_message)
            raise forms.ValidationError(error_message)

        return self.cleaned_data
