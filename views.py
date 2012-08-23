from django import http

#import logging

# Create your views here.
def set_currency(request):
    """
    Just remember currency in session or cookie.
    Redirect to a given url while setting the chosen currency in the
    session or cookie. The url and the currency code need to be
    specified in the request parameters.
    """
    next = request.REQUEST.get('next', None)
    if not next:
        next = request.META.get('HTTP_REFERER', None)
    if not next:
        next = '/'
    response = http.HttpResponseRedirect(next)
    if request.method == 'POST':
        currency_code = request.POST.get('currency', None)
        if currency_code:
            if hasattr(request, 'session'):
                request.session['django_currency'] = currency_code
            else:
                response.set_cookie(settings.CURRENCY_COOKIE_NAME, currency_code)

    #return http.HttpResponse(request.POST)
    return response

