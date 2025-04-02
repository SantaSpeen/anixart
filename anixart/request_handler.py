# -*- coding: utf-8 -*-

import logging

import requests

from .__meta__ import __version__, __build__
from .endpoints import API_URL
from .exceptions import AnixartAPIRequestError, AnixartAPIError
_log_name = "file:%-28s -> %s" % ("<Anixart.request_handler:%-3i>", "%s")


def _parse_res_code(res, payload, http_method, http_headers):
    json = res.json()
    error = json.get("error")
    code = json.get("code")
    if res.status_code >= 400:
        raise AnixartAPIRequestError(f"\n\nAnixartPyAPIWrapper: ERROR\n"
                                     f"Send this info to author: https://t.me/SantaSpeen\n"
                                     f"URL: {http_method} {res.url}\n"
                                     f"Status code: {res.status_code}\n"
                                     f"Res headers: {res.headers}\n"
                                     f"Req headers: {http_headers}\n"
                                     f"Server res: {json}\n"
                                     f"Client req: {payload}\n")
    if error:
        raise AnixartAPIRequestError(f"Internal server error: {error}; Payload: {payload}")
    if code:
        if code == 0:
            return
        else:
            raise AnixartAPIError(f"AnixartAPI send error code: {code}; Json: {json}")


class AnixartRequestsHandler:

    def __init__(self, token: str = None, session: requests.Session = None,
                 _log_class="Anixart.request_handler.AnixartRequestsHandler"):
        self.__log = logging.getLogger(_log_class)
        self.__log.debug(_log_name, 44, f"__init__ - INIT from {self}")
        if session:
            self.__session = session
        else:
            self.__log.debug(_log_name, 48, "Create new session.")
            self.__session = requests.Session()
        self.__session.headers = {
            'User-Agent': f'AnixartPyAPIWrapper/{__version__}-{__build__}'
                          f' (Linux; Android 12; SantaSpeen AnixartPyAPIWrapper Build/{__build__})'}
        self.__token = token

    def post(self, method: str, payload: dict = None, is_json: bool = False, **kwargs):
        if payload is None:
            payload = {}
        url = API_URL + method
        if payload.get("token") is None:
            if self.__token is not None:
                payload.update({"token": self.__token})
                url += "?token=" + self.__token
        else:
            token = kwargs.get("token")
            if token is not None:
                payload.update({"token": token})
                url += "?token=" + token
        kwargs = {"url": url}
        if is_json:
            self.__session.headers.update({"Content-Type": "application/json; charset=UTF-8"})
            self.__session.headers.update({"Content-Length": str(len(str(payload)))})
            kwargs.update({"json": payload})
        else:
            kwargs.update({"data": payload})
        self.__log.debug(_log_name, 79, f"{'json' if is_json else ''} POST {method}; {payload}")
        res = self.__session.post(**kwargs)
        _parse_res_code(res, payload, "POST", self.__session.headers)
        self.__session.headers["Content-Type"] = ""
        self.__session.headers["Content-Length"] = ""
        return res

    def get(self, method: str, payload: dict = None, **kwargs):
        if payload is None:
            payload = {}
        if payload.get("token") is None:
            if self.__token is not None:
                payload.update({"token": self.__token})
        else:
            token = kwargs.get("token")
            if token is not None:
                payload.update({"token": token})
        self.__log.debug(_log_name, 101, f"GET {method}; {payload}")
        res = self.__session.get(API_URL + method, params=payload)
        _parse_res_code(res, payload, "GET", self.__session.headers)
        return res
