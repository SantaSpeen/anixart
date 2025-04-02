import json
from pathlib import Path

import requests

from anixart.exceptions import AnixartInitError


class AnixartAccount:
    def __init__(self, username: str, password: str):
        self._username = username
        self._password = password
        if not isinstance(username, str) or not isinstance(password, str):
            raise AnixartInitError("Auth data must be strings.")

        self._token = None
        self._session = requests.Session()

    @property
    def username(self):
        return self._username

    @property
    def session(self):
        return self._session

    @property
    def token(self):
        return self._token

    def to_file(self, filename: str | Path):
        """Save the account information to a file."""
        acc = AnixartAccountSaved.from_account(filename, self)
        acc.save()
        return acc

    @classmethod
    def from_file(cls, filename: str | Path):
        """Load the account information from a file."""
        acc = AnixartAccountSaved(filename)
        acc.load()
        return acc

    def login(self):
        """Login to Anixart and return the token."""
        # TODO: Implement login logic here

    def __str__(self):
        return f'AnixartAccount(login={self._username!r}, password={"*" * len(self._password)!r})'

    def __repr__(self):
        return f"<{self}>"

class AnixartAccountSaved(AnixartAccount):

    def __init__(self, account_file: str | Path = "anixart_account.json"):
        super().__init__("", "")
        self._file = Path(account_file)

    def save(self):
        """Save the account information to a file."""
        data = {
            "username": self._username,
            "password": self._password,
            "token": self._token
        }
        with open(self._file, 'w') as f:
            json.dump(data, f, indent=4)

    def load(self):
        """Load the account information from a file."""
        if not self._file.exists():
            raise AnixartInitError(f"Account file {self._file} does not exist.")
        with open(self._file, 'r') as f:
            data = json.load(f)
            self._username = data.get("username")
            self._password = data.get("password")
            self._token = data.get("token")
        if not self._username or not self._password:
            raise AnixartInitError("Login and password must be provided in the account file.")

    @classmethod
    def from_account(cls, account_file: str | Path, account: AnixartAccount):
        c = cls(account_file)
        c._username = account.username
        c._password = account._password
        c._token = account.token
        return c

    def login(self):
        """Login to Anixart using the saved credentials."""
        # Проверяем токен, если просрочен, то логинимся
        # Если токен валиден, то просто дальше работаем
        # TODO: Implement login logic here
        pass

    def __str__(self):
        return f'AnixartAccountSaved(account_file={self._file!r}")'

class AnixartAccountToken(AnixartAccount):

    def __init__(self, token):
        super().__init__("mradx", "")  # Пасхалка)
        self._token = token

    def login(self):
        """Login to Anixart and return information about the tokens."""
        # TODO: Implement login logic here
        pass

    def __str__(self):
        return f'AnixartAccountToken(token={self._token!r}")'
