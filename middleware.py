"This is the locale selecting middleware that will look at accept headers"

import logging
from django.conf import settings

class CurrencyLocaleMiddleware(object):
    """
    This is a very simple middleware that parses a request
    and decides what currenct install as default if there is none selected
    """

    def process_request(self, request):
        if hasattr(request, 'session'):
            if request.session.get('django_currency') is None:
                request.session['django_currency'] = settings.DEFAULT_CURRENCY
