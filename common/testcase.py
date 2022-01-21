import logging

from django.conf import settings
from django.test import TestCase, TransactionTestCase


class _BaseTestDatabaseDescriptor:
    def __get__(self, instance, cls=None):
        return set(settings.DATABASES.keys())


class BaseTestCase(TestCase):
    databases = _BaseTestDatabaseDescriptor()

    def setUp(self):
        logging.disable(logging.WARNING)

    def tearDown(self):
        logging.disable(logging.NOTSET)
