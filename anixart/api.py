# -*- coding: utf-8 -*-
import requests

from .__meta__ import __version__, __build__
from .auth import AnixartAccount, AnixartAccountGuest
from .enums import AnixartApiErrors
from .endpoints import API_URL
from .exceptions import AnixartAPIRequestError, AnixartAPIError
from .exceptions import AnixartInitError


class AnixartAPI:

    def __init__(self, account: AnixartAccount = None):
        if account is None:
            account = AnixartAccountGuest()
        if not isinstance(account, AnixartAccount):
            raise AnixartInitError(f'Use class "AnixartAccount" for user. But {type(account)} given.')

        self.use_account(account)

    def use_account(self, account: AnixartAccount):
        if not isinstance(account, AnixartAccount):
            raise AnixartInitError(f'Use class "AnixartAccount" for user. But {type(account)} given.')
        self.__account = account
        self.__account._set_api(self)
        self.__account.login()

        self.__token = account.token
        self._session = account.session
        self._session.headers = {
            'User-Agent': f'AnixartPyAPI/{__version__}-{__build__} (Linux; Android 15; AnixartPyAPI Build/{__build__})'
        }

    @property
    def account(self):
        return self.__account

    def __parse_response(self, res: requests.Response):
        if res.status_code != 200:
            e = AnixartAPIRequestError("Bad Request: Invalid request parameters.")
            e.message = (
                f"Bad Request: Invalid request parameters.\n"
                f"Request: {res.request.method} {res.url}\n"
                f"Status code: {res.status_code}\n"
                f"Response: {res.text}\n"
                f"Client headers: {self._session.headers}\n"
                f"Client payload: {res.request.body}"
            )
            e.code = 400
            raise e
        if not res.text:
            raise AnixartAPIError("AnixartAPI send unknown error: Empty response. Is provided data correct?")
        try:
            response = res.json()
        except ValueError as e:
            raise AnixartAPIError("Failed to parse JSON response")

        # print(response)
        if response['code'] != 0:
            code = response['code']
            if code in AnixartApiErrors:
                e = AnixartAPIError(f"AnixartAPI send error: {AnixartApiErrors(code).name}")
                e.message = AnixartApiErrors(code).name
            else:
                e = AnixartAPIError(f"AnixartAPI send unknown error, code: {response['code']}")
            e.code = response['code']
            raise e

        return response

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
            self._session.headers["Content-Type"] = "application/json; charset=UTF-8"
            self._session.headers["Content-Length"] = str(len(payload))
            kwargs.update({"json": payload})
        else:
            kwargs.update({"data": payload})
        res = self._session.post(**kwargs)
        self._session.headers["Content-Type"] = ""
        self._session.headers["Content-Length"] = ""
        return self.__parse_response(res)

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
        res = self._session.get(API_URL + method, params=payload)
        return self.__parse_response(res)

    def execute(self, http_method, endpoint, **kwargs):
        http_method = http_method.upper()
        if http_method == "GET":
            return self.get(endpoint, **kwargs)
        elif http_method == "POST":
            return self.post(endpoint, **kwargs)
        else:
            raise AnixartAPIRequestError("Allow only GET and POST requests.")

    def __str__(self):
        return f'AnixartAPI(account={self.__account!r})'

    def __repr__(self):
        return f"<{self}>"
