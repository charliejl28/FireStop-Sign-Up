# -*- coding: utf-8 -*-
import json
from webapp.tests import TestViews
from django.core.urlresolvers import reverse

from .models import Guest


class TestUsers(TestViews):
    def setUp(self):
        super(TestUsers, self).setUp()
        self.data = {
            'name': 'John Smith',
            'position': 'Position',
            'department': 'New York City Fire Department',
            'email': 'contact@johnsmith.com'
        }

    def test_signup(self):
        """
        As a guest I should be able to register in the page to let it know that
        I'm interested in using the app.
        """

        # counts the initial guests objects
        count_initial = Guest.objects.count()

        # sends the post request with the data
        response = self.post_ajax(reverse('signup'), json.dumps(self.data), 
                                  content_type="application/json")
        assert response['success']

        # Checks if a guest object was inserted
        assert Guest.objects.count() == count_initial + 1

    def test_all_fields_are_required(self):
        """
        As a guest I should enter all fields to signup.
        """

        for field in self.data.keys():
            # Create the data with the current field in blank.
            data = self.data.copy()
            data[field] = ''

            # Sends the response and checks the NOT success
            response = self.post_ajax(reverse('signup'), json.dumps(data),
                                      content_type="application/json")
            assert not response['success']
