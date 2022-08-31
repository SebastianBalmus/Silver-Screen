from django.shortcuts import render
from ratelimit.decorators import ratelimit
from django.core.exceptions import ObjectDoesNotExist
from newsletter.forms import NewsletterRegistrationForm
from newsletter.models import SubscribedUser


@ratelimit(key='ip', rate='10/m', method='POST', block=True)
def subscribe(request):

    if request.user.is_authenticated:

        email = request.user.email

        try:
            SubscribedUser.objects.get(email=email)
            return render(request, 'newsletter/already_subscribed.html')

        except ObjectDoesNotExist:

            SubscribedUser.objects.create(email=email)
            return render(request, 'newsletter/success.html')
    else:

        if request.method == 'POST':
            form = NewsletterRegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                return render(request, 'newsletter/success.html')

        else:
            form = NewsletterRegistrationForm()

    context = {
        'form': form,
    }

    return render(request, 'newsletter/subscription_form.html', context)


def unsubscribe(request, pk):
    status = SubscribedUser.objects.filter(id=pk).delete()
    if status[0] == 0:
        return render(request, 'newsletter/already_unsubscribed.html')
    return render(request, 'newsletter/unsubscribe_successful.html')

