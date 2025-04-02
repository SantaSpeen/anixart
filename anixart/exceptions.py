# -*- coding: utf-8 -*-

class AnixartBasError(Exception): ...

# Init errors

class AnixartInitError(AnixartBasError, TypeError): ...

# API errors
class AnixartAPIError(AnixartBasError):
    message = "unknown error"
    code = 0

class AnixartAuthError(AnixartAPIError): ...

class AnixartAPIRequestError(AnixartAPIError): ...

