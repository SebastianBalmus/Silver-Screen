from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .forms import UserRegisterForm
from django.contrib.auth import get_user_model
from ratelimit.decorators import ratelimit
from .token import account_activation_token


@ratelimit(key='ip', rate='1/h', method='POST', block=True)
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
            return redirect(register_sent)
    else:
        form = UserRegisterForm()
    return render(
        request=request,
        template_name="registration/register.html",
        context={"register_form": form}
    )


@ratelimit(key='ip', rate='1/h', method='POST', block=True)
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


def register_sent(request):
    return render(request, 'registration/registration_email_sent.html')
