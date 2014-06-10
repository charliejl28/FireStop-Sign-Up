# -*- coding: utf-8 -*-
from django.views.generic.edit import CreateView
from webapp.views import JSONResponseMixin

from .models import Guest


class SignupView(JSONResponseMixin, CreateView):
    model = Guest

    def form_valid(self, form):
        """
        If the form is valid stores the object and return success
        """

        # stores the object
        self.object = form.save()

        # send the json response
        return self.json_response({'success': True})

    def form_invalid(self, form):
        """
        If the form is invalid return not success and errors found.
        """

        # send the json response and errors
        return self.json_response({'success': False, 'errors': form.errors})
