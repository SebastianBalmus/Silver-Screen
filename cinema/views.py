from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

import cinema.views
from .forms import ContactForm, UserRegisterForm
from django.contrib.auth import login, get_user_model
from django.contrib import messages

# Homepage view
from .token import account_activation_token


def home(request):
    return render(request, 'home.html')


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


def register_request(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Account activation'
            message = render_to_string(
                'registration/registration_email.html',
                {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                }
            )
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return redirect(cinema.views.home)
    else:
        form = UserRegisterForm()
    return render(
        request=request,
        template_name="registration/register.html",
        context={"register_form": form}
    )


def activate_account(request, uidb64, token):
    user = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = user.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'registration/registration_complete.html')
    else:
        return render(request, 'registration/registration_complete.html')
