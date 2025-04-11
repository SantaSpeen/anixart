# -*- coding: utf-8 -*-

class AnixartBaseError(Exception): ...

# Init errors

class AnixartInitError(AnixartBaseError, TypeError): ...

# API errors
class AnixartAPIError(AnixartBaseError):
    message = "unknown error"
    code = 0

class AnixartAuthError(AnixartAPIError): ...

class AnixartAPIRequestError(AnixartAPIError): ...

