currecies-for-django
====================

This simple app will add currecies list, some templatetags and post handler which will switch currency and save that selection in user session.

Currency list based on:
http://download.geonames.org/export/dump/countryInfo.txt
A list of currency symbols is available here : http://forum.geonames.org/gforum/posts/list/437.page
This one taken !!!!!!!!!!!!!!
another list with fractional units is here: http://forum.geonames.org/gforum/posts/list/1961.page	

Install:
Check out this app as 'currencies'

Configuration:
Add the currencies you need to your settings.py as well as cookie name (session storage is defult)

    CURRENCY_COOKIE_NAME = 'django_currency'
    CURRENCIES = (
    	 ('AED', gettext('United Arab Emirates dirham')),
    	 ('AFN', gettext('Afghan afghani')),
    	 ('ALL', gettext('Albanian lek')),
    	 ('USD', gettext('USD dollar')),
	 )
    )

Next add urls with prefix of yours choice
    (r'^currency/', include('curriences.urls')),

Finally enable curriences in settings.py

	INSTALLED_APPS = (
	     ...      
    	     'currencies',      
	     ...
    	     # 'django.contrib.admindocs',
	)

Usage:
Create post form:
       {% load currencies %}

       {% get_current_currency as currency %}
       {% get_available_currencies as CURRENCIES %}

       {% get_currency_info_list for CURRENCIES as currencies %}
       <form action="/currency/setcurrency/" method="post" name="currencies"> 
	 {% csrf_token %}
	 <!--- <input name="next" type="hidden" value="/friend/invite/" /> -->
	 <select name="currency">
	   {% for c in currencies %}
	   {% ifequal c.code currency %}
	   <option selected="true" value="{{ c.code }}">{{ c.name }}</option>
	   {% else %}
	   <option value="{{ c.code }}">{{ c.name }}</option>
	   {% endifequal %}
	   {% endfor %}
	 </select>
	 <input type="submit" value="Switch Currency"/>
       </form> 

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
