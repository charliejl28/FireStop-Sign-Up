"""
Copyright (c) 2013 Jose Maria Zambrana <contact@josezambrana.com>

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""

import logging
import json

from django.db import models
from django import forms
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpRequest, Http404, HttpResponse
from django.views.generic import View, TemplateView
from django.views.generic.base import TemplateResponseMixin
from django.utils.translation import ugettext_lazy as _


logger = logging.getLogger('project.verbose')


class MessagesMixin(object):
    """
    Handle messages name->value in the class.
    """

    messages = (
        ('success', _('Performed successfully!')),
        ('fail', _('Something went wrong'))
    )

    @classmethod
    def get_messages(cls):
        """
        Returns a dictionary with the messages for this view.
        """

        if not hasattr(cls, '_messages'):
            messages = tuple()

            # Gets messages from parents.
            for parent in reversed(cls.mro()):
                messages += getattr(parent, 'messages', tuple())

            #  Adds messages from the current class.
            messages += getattr(cls, 'messages', tuple())

            # Creates the dictionary and cache
            cls._messages = dict(messages)

        return cls._messages

    @classmethod
    def get_message(cls, name):
        """
        Return the message with the passed name.
        """

        messages = cls.get_messages()

        # returns if exist
        if (name in messages):
            return messages.get(name)

        # raises error if the message does not exist
        raise ValueError('%(name)s is not defined in %(cls)s.messages' % {
            'name': name,
            'cls': cls.__name__
        })


class LoginRequiredMixin(object):
    #: Does the class need login?
    login_required = False

    def dispatch(self, request, *args, **kwargs):
        """
        Dispatch the request and verifies if the view requires login.
        If login is required, it creates a response with the login url and
        success flag as false.
        """

        # verifies if login is required
        if self.login_required and not request.user.is_authenticated():
            return login_required_response(request, *args, **kwargs)

        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)

    def login_required_response(self, request, *args, **kwargs):
        raise NotImplementedError

    def get_login_url(self, request):
        """
        Returns the login url with the called url as a next step after login.
        """

        login_url_parts = list(urlparse.urlparse(reverse('account_login')))

        querystring = QueryDict(login_url_parts[4], mutable=True)
        querystring[REDIRECT_FIELD_NAME] = request.get_full_path()
        login_url_parts[4] = querystring.urlencode(safe='/')

        return urlparse.urlunparse(login_url_parts)


class JSONResponseMixin(object):
    """
    Mixin to return response in json for class-based views.
    """

    def needs_login_response(self, request, *args, **kwargs):
        context = {
            'success': False,
            'message': _(u'Login is required'),
            'redirect_url': self.get_login_url(request)
        }

        return self.json_response(context, status=401)

    def is_serializable(self, value):
        """
        Verifies if value is an instance of a Model, Request or Model, they
        can't be serialized by simplejson
        """

        is_model = isinstance(value, models.Model)
        is_request = isinstance(value, HttpRequest)
        is_form = isinstance(value, forms.BaseForm)

        return not is_model and not is_request and not is_form

    def json_response(self, context, **response_kwargs):
        """
        Creates a response in json format with the context's values.
        """

        if isinstance(context, dict):
            for key, value in context.items():
                if not self.is_serializable(value) or key == 'view':
                    del context[key]

        context_json = json.dumps(context, cls=DjangoJSONEncoder)
        response_kwargs['content_type'] = "application/json"

        return HttpResponse(context_json, **response_kwargs)


class JSONView(JSONResponseMixin, View):
    def get_context_data(self, **kwargs):
        return kwargs

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.json_response(context)


class MultipleFormatMixin(MessagesMixin, LoginRequiredMixin, JSONResponseMixin,
                          TemplateResponseMixin):
    """
    Base to speak more than one format.
    """

    # returns in json format on ajax calls.
    json_in_ajax = True
    format_response = None

    def get_response_format(self):
        """
        returns the format that will be use in the response.
        """

        if self.format_response is not None:
            return self.format_response

        format_response = self.request.REQUEST.get('format', 'html')

        return format_response

    def html_response(self, context, **kwargs):
        """
        renders the response in html using a template
        """

        return TemplateResponseMixin.render_to_response(self, context, **kwargs)

    def is_json(self):
        """
        Does the response should be JSON?
        """

        format_response = self.get_response_format()

        return (self.request.is_ajax() and self.json_in_ajax) \
                or format_response == 'json'

    def render_to_response(self, context, **kwargs):
        """
        Renders the response to the format requested, html by default.
        """

        format_response = self.get_response_format()

        # JSON format?
        if self.is_json():
            logger.info('json')
            return self.json_response(context, **kwargs)

        # HTML format?
        elif format_response == 'html':
            logger.info('html')
            return self.html_response(context, **kwargs)

        raise Http404


class MultipleFormatView(MultipleFormatMixin, TemplateView):
    pass
