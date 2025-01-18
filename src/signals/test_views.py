from http import HTTPStatus

import factory
from django.contrib.auth.models import User
from django.urls import reverse
from factory.django import DjangoModelFactory
from rest_framework.test import APITestCase

from . import models
from . import views


class UserFactory(DjangoModelFactory):
    email = 'user@example.com'
    username = 'user'
    password = factory.PostGenerationMethodCall('set_password', 'adm1n')

    class Meta:
        model = User


class FlagFactory(DjangoModelFactory):
    name = "test"
    description = "description"

    class Meta:
        model = models.Flag


class TestFlagAPIView(APITestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = UserFactory.create()

    def test_get_ok_for_enabled(self):
        flag = FlagFactory(author=self.user, is_enabled=True)
        self.__test_get_found(flag, HTTPStatus.OK)

    def test_get_no_content_for_disabled(self):
        flag = FlagFactory(author=self.user)
        self.__test_get_found(flag, HTTPStatus.NO_CONTENT)

    def test_get_not_found_for_non_existent(self):
        url = reverse("signals:flag", kwargs={"name": "non_existent"})
        response = self.client.get(url)
        response.render()
        self.assertEqual(HTTPStatus.NOT_FOUND, response.status_code)
        self.assertEqual(b'', response.content)
        self.assertNotIn(views.HEADERS_X_LIGHTS_UPDATED_AT, response.headers.keys())

    def __test_get_found(self, flag: models.Flag, status: HTTPStatus):
        url = reverse("signals:flag", kwargs={"name": flag.name})
        response = self.client.get(url)
        response.render()
        self.assertEqual(status, response.status_code)

        self.assertEqual(b'', response.content)
        header_value = response.headers.get(views.HEADERS_X_LIGHTS_UPDATED_AT)
        self.assertEqual(header_value, str(flag.updated_at.microsecond))