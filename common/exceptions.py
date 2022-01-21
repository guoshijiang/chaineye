# -*- coding: utf-8 -*-

import logging
from urllib.parse import unquote


class BaseException(Exception):
    message = "An unknown exception occurred."
    code = 400

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs

        if 'code' not in self.kwargs and hasattr(self, 'code'):
            self.kwargs['code'] = self.code

        if message:
            self.message = unquote(message)

        try:
            self.message = self.message % kwargs
        except Exception as e:
            # kwargs doesn't match a variable in the message
            # log the issue and the kwargs
            logging.exception('Exception in string format operation, kwargs: %s', self.message)
            raise e

        super(BaseException, self).__init__()

    def __str__(self):
        return self.message


class NotFound(BaseException):
    message = "Resource could not be found."
    code = 404


class AccessForbidden(BaseException):
    message = "Access Forbidden"
    code = 403


class Unauthorized(BaseException):
    message = "Not Authorized"
    code = 401


class Conflict(BaseException):
    message = 'Conflict.'
    code = 409


class TableCreateError(BaseException):
    message = "Table Create Error"
    code = 1001

