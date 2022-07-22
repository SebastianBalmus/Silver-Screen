from django.http import HttpResponseForbidden
from django.shortcuts import render
from ratelimit.exceptions import Ratelimited


def handler403(request, exception=None):
    if isinstance(exception, Ratelimited):
        return render(request, 'errors/rate_limit_exceeded.html')
    return HttpResponseForbidden('Forbidden')
