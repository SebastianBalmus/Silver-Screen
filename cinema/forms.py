from django import forms


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
