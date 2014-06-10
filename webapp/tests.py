import logging
import json

from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client


class TestBase(TestCase):
    def setUp(self):
        self.logger = logging.getLogger('project.verbose')

    def _info(self, message):
        self.logger.info(message)


class TestViews(TestBase):
    secure = False

    def setUp(self):
        self.client = Client()
        self.login_url = reverse('admin:index')
        self.logout_url = reverse('admin:logout')
        super(TestViews, self).setUp()

    def _login(self):
        response = self.post(self.login_url, self.login_data)
        self._info('response login: %s' % response)
        assert response.status_code == 302
        return response

    def _logout(self):
        response = self.get(self.logout_url)
        assert response.status_code == 302
        return response

    def get(self, path, *args, **kwargs):
        if self.secure:
            kwargs['wsgi.url_scheme'] = 'https'

        return self.client.get(path, *args, **kwargs)

    def post(self, path, *args, **kwargs):
        if self.secure:
            kwargs['wsgi.url_scheme'] = 'https'

        return self.client.post(path, *args, **kwargs)

    def put(self, path, *args, **kwargs):
        if self.secure:
            kwargs['wsgi.url_scheme'] = 'https'

        return self.client.put(path, *args, **kwargs)

    def delete(self, path, *args, **kwargs):
        if self.secure:
            kwargs['wsgi.url_scheme'] = 'https'

        return self.client.delete(path, *args, **kwargs)

    def get_ajax(self, path, *args, **kwargs):
        kwargs['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        response = self.get(path, *args, **kwargs)
        self._info('%s GET %s' % (response.status_code, path))
        return json.loads(response.content)

    def post_ajax(self, path, *args, **kwargs):
        kwargs['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        response = self.post(path, *args, **kwargs)
        self._info('%s POST %s' % (response.status_code, path))
        return json.loads(response.content)

    def put_ajax(self, path, *args, **kwargs):
        kwargs['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        response = self.put(path, *args, **kwargs)
        self._info('%s PUT %s' % (response.status_code, path))
        return json.loads(response.content)

    def delete_ajax(self, path, *args, **kwargs):
        kwargs['HTTP_X_REQUESTED_WITH'] = 'XMLHttpRequest'
        response = self.delete(path, *args, **kwargs)
        self._info('%s DELETE %s' % (response.status_code, path))
        return json.loads(response.content)
