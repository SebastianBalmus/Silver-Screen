from django.shortcuts import render
from .forms import ContactForm


# Homepage view
def home(request):
    return render(request, 'home.html', {})


# Contact view
def contact(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST)
        if contact_form.is_valid():
            contact_form.save()
            return render(request, 'home.html')
    else:
        contact_form = ContactForm()

    context = {'form': contact_form}
    return render(request, 'contact.html', context)
