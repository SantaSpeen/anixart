# -*- coding: utf-8 -*-

import requests

from .__meta__ import __version__, __build__
from .auth import AnixartAccount, AnixartAccountGuest
from .endpoints_map import endpoints_map
from .exceptions import AnixartAPIRequestError, AnixartAPIError
from .exceptions import AnixartInitError

debug = True

class _ApiMethodGenerator:
    def __init__(self, start_path, _callback: callable):
        self._path = start_path
        self._callback = _callback

    def __setattr__(self, __name, __value):
        raise TypeError(f"cannot set '{__name}' attribute of immutable type 'ApiMethodGenerator'")

    def __getattr__(self, item):
        self._path += f".{item}"
        return self

    def __call__(self, *args, **kwargs):
        if debug:
            print(f"[D] __call__ -> {self._path} args={args} kwargs={kwargs}")
        return self._callback(self._path, *args, **kwargs)

    def __str__(self):
        return f"ApiMethodGenerator(path={self._path!r})"

    def __repr__(self):
        return f"<{self}>"

class AnixartAPI:

    API_URL = "https://api.anixart.tv"

    def __init__(self, account: AnixartAccount = None):
        if account is None:
            account = AnixartAccountGuest()
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
        if debug:
            print(f"[D] -> {res.request.method} body='{res.request.body!s}' url='{res.url!s}'")
            print(f"[D] <- {res.status_code}, {len(res.text)=}")
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

        if debug:
            print(response)
        if response['code'] != 0:
            e = AnixartAPIError(f"AnixartAPI send unknown error, code: {response['code']}")
            e.code = response['code']
            raise e

        return response

    def _post(self, method: str, _json: bool = False, **kwargs):
        url = self.API_URL + method
        kwargs["token"] = kwargs.get("token", self.__token)
        if kwargs["token"]:
            url += f"?token={self.__token}"

        req_settings = {"url": url}
        if _json:
            self._session.headers["Content-Type"] = "application/json; charset=UTF-8"
            req_settings.update({"json": kwargs})
        else:
            req_settings.update({"data": kwargs})
        res = self._session.post(**req_settings)
        return self.__parse_response(res)

    def _get(self, method: str, **kwargs):
        if self.__token:
            kwargs["token"] = kwargs.get("token", self.__token)

        res = self._session.get(self.API_URL + method, params=kwargs)
        return self.__parse_response(res)

    def _execute(self, http_method, endpoint, **kwargs):
        http_method = http_method.upper()
        if http_method == "GET":
            return self._get(endpoint, **kwargs)
        elif http_method == "POST":
            return self._post(endpoint, **kwargs)
        else:
            raise AnixartAPIRequestError("Allow only GET and POST requests.")

    def __execute_endpoint_from_map(self, key, *args, **kwargs):
        endpoint = endpoints_map.get(key)
        if endpoint is None:
            raise AnixartAPIError("Invalid endpoint.")
        return self._execute_endpoint(endpoint, *args, **kwargs)

    def _execute_endpoint(self, endpoint, *args, **kwargs):
        req_settings, headers = endpoint.build_request(*args, **kwargs)
        self._session.headers.update(headers)
        if endpoint.is_post:
            res = self._session.post(**req_settings)
        else:
            res = self._session.get(**req_settings)
        return self.__parse_response(res)

    def get(self, endpoint, *args, **kwargs):
        return self._execute("GET", endpoint.format(*args), **kwargs)

    def post(self, endpoint, *args, **kwargs):
        return self._execute("POST", endpoint.format(*args), **kwargs)

    def __getattr__(self, item):
        return _ApiMethodGenerator(item, self.__execute_endpoint_from_map)

    def __str__(self):
        return f'AnixartAPI(account={self.__account!r})'

    def __repr__(self):
        return f"<{self}>"
