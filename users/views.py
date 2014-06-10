# -*- coding: utf-8 -*-
import json

from django.views.generic.edit import CreateView
from webapp.views import JSONResponseMixin

from .models import Guest


class SignupView(JSONResponseMixin, CreateView):
    model = Guest
    template_name = 'users/signup.html'

    def get_form_kwargs(self):
        kwargs = super(SignupView, self).get_form_kwargs()

        if self.request.method == 'POST':
            kwargs['data'] = json.loads(self.request.body)

        return kwargs

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
        return self.json_response({'success': False, 'errors': form.errors},
                                  status=400)
