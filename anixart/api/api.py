import logging

import requests

from ..auth import AnixartAuth
from ..errors import AnixartInitError, AnixartAPIRequestError
from ..request_handler import AnixartRequestsHandler

_log_name = "file:%-29s -> %s" % ("<anixart.api:%-4i>", "%s")


class AnixartUserAccount:
    def __init__(self, login, password, config_file="anixart_data.json", **kwargs):
        self.kwargs = kwargs
        log_level = logging.CRITICAL
        log_format = '[%(name)-43s] %(levelname)-5s: %(message)s'
        if kwargs.get("loglevel") is not None:
            log_level = kwargs.get("loglevel")
        if kwargs.get("logformat") is not None:
            log_format = kwargs.get("logformat")
        logging.basicConfig(level=log_level, format=log_format)
        init_log = logging.getLogger("anixart.api.AnixUserAccount")
        init_log.debug(_log_name, 23, "__init__ - INIT")
        self.login = login
        self.password = password
        if not isinstance(login, str) or not isinstance(password, str):
            raise AnixartInitError("Use normal auth data. In string.")
        self.token = None
        self.id = None
        self.config_file = config_file
        self.session = requests.Session()
        init_log.debug(_log_name, 32, f"{str(self)}")
        init_log.debug(_log_name, 33, "__init__() - OK")

    def __str__(self):
        return f'AnixartUserAccount(login="{self.login}", password="{self.password}", ' \
               f'config_file="{self.config_file}", kwargs="{self.kwargs}")'

    def get_login(self):
        return self.login

    def get_password(self):
        return self.password

    def get_token(self):
        return self.token

    def get_id(self):
        return self.id


class AnixartAPI:

    def __init__(self, user: AnixartUserAccount):
        init_log = logging.getLogger("anixart.api.AnixartAPI")
        init_log.debug(_log_name, 56, "__init__ - INIT")
        if not isinstance(user, AnixartUserAccount):
            init_log.critical('Use anixart.api.AnixartUserAccount for user.')
            raise AnixartInitError('Use class "AnixartUserAccount" for user.')
        self.auth = AnixartAuth(user)
        if user.token is None or user.id is None:
            init_log.debug(_log_name, 62, "Singing in..")
            self.auth.sing_in()
        self.user = user
        init_log.debug(_log_name, 65, "__init__ - OK.")
        self.http_handler = AnixartRequestsHandler(user.token, user.session)

    def __str__(self):
        return f'AnixAPI({self.user})'

    def execute(self, http_method, endpoint, **kwargs):
        http_method = http_method.upper()
        if http_method == "GET":
            return self.http_handler.get(endpoint, **kwargs)
        elif http_method == "POST":
            return self.http_handler.post(endpoint, **kwargs)
        else:
            raise AnixartAPIRequestError("Allow only GET and POST requests.")
