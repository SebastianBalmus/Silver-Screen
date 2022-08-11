from django import forms

from .models import Contact, Schedule, CinemaHall
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

        if not self.cleaned_data['name'].isalpha():
            error_message = 'Your name can\'t contain numbers!'
            self.add_error('name', error_message)
            raise forms.ValidationError(error_message)

        return self.cleaned_data


class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ScheduleForm, self).__init__(*args, **kwargs)
        self.fields['hall'].queryset = CinemaHall.objects.none()
        if 'cinema' in self.data:
            try:
                cinema_id = self.data.get('cinema')
                self.fields['hall'].queryset = CinemaHall.objects.filter(cinema_id=cinema_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['hall'].queryset = self.instance.cinema.halls.order_by('name')
