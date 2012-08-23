from django.template import (Node, Variable, TemplateSyntaxError, TokenParser, Library, TOKEN_TEXT, TOKEN_VAR)
from django.utils import translation

from pprint import pprint
from pprint import pformat

import logging

from django.contrib.sessions.backends.db import SessionStore

from ..locale.currencies_info import CURRENCY_INFO

register = Library()

class GetAvailableCurrenciesNode(Node):
    def __init__(self, variable):
        self.variable = variable

    def render(self, context):
        from django.conf import settings
        context[self.variable] = [(k, translation.ugettext(v)) for k, v in settings.CURRENCIES]
        return ''

class GetCurrentCurrencyNode(Node):
    def __init__(self, variable):
        self.variable = variable

    def get_current_currency(self, context):
        return context.get('request').session.get('django_currency')

    def render(self, context):
        context[self.variable] = self.get_current_currency(context)
        return ''

class GetCurrencyInfoListNode(Node):
    def __init__(self, currencies, variable):
        self.currencies = Variable(currencies)
        self.variable = variable

    def get_currency_dict(self,currency_code):
        try:
            return CURRENCY_INFO[currency_code]
        except KeyError:
            #pass
            raise KeyError("Unknown language code %r." % currency_code)

    def get_currency_info(self, currency):
        # ``currency`` is either a currency code string or a sequence
        # with the language code as its first item
        if len(currency[0]) > 1:
            return self.get_currency_dict(currency[0])
        else:
            return self.get_currency_dict(str(currency))

    def render(self, context):
        currencies = self.currencies.resolve(context)
        context[self.variable] = [self.get_currency_info(c) for c in currencies]
        return ''

@register.tag("get_current_currency")
def do_get_current_currency(parser, token):
    """
    This will store the current currency in the context.

    Usage::

        {% get_current_currency as currency %}

    This will fetch the currently active currency and
    put it's value into the ``currency`` context
    variable.
    """
    args = token.contents.split()
    if len(args) != 3 or args[1] != 'as':
        raise TemplateSyntaxError("'get_current_currency' requires 'as variable' (got %r)" % args)
    return GetCurrentCurrencyNode(args[2])

@register.tag("get_currency_info_list")
def do_get_currency_info_list(parser, token):
    """
    This will store a list of currency information dictionaries for the given
    currency codes in a context variable. The currency codes can be specified
    either as a list of strings or a settings.CURRENCIES style tuple (or any
    sequence of sequences whose first items are currency codes).

    Usage::

        {% get_currency_info_list for CURRENCIES as currencies %}
        {% for c in currencies %}
          {{ c.code }}
          {{ c.name }}
          {{ c.symbol }}
          {{ c.cent_name }}
        {% endfor %}
    """
    args = token.contents.split()
    if len(args) != 5 or args[1] != 'for' or args[3] != 'as':
        raise TemplateSyntaxError("'%s' requires 'for sequence as variable' (got %r)" % (args[0], args[1:]))

    return GetCurrencyInfoListNode(args[2], args[4])

@register.tag("get_available_currencies")
def do_get_available_currencies(parser, token):
    """
    This will store a list of available currencies
    in the context.

    Usage::

        {% get_available_currencies as currencies %}
        {% for currency in currencies %}
        ...
        {% endfor %}

    This will just pull the CURRENCIES setting from
    your setting file (or the default settings) and
    put it into the named variable.
    """
    args = token.contents.split()
    if len(args) != 3 or args[1] != 'as':
        raise TemplateSyntaxError("'get_available_currencies' requires 'as variable' (got %r)" % args)
    return GetAvailableCurrenciesNode(args[2])

