from dataclasses import dataclass

from anixart.exceptions import AnixartAuthError
from anixart.utils import BaseParseFactory


@dataclass
class _AuthLoginFactoryProfileToken:
    # { "id": 1, "token": "hash?" }
    id: int  # token id?
    token: str  # token str

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data.get("id", -1),
            token=data.get("token")
        )


@dataclass
class AuthLoginFactory(BaseParseFactory):
    # { "code": 0, "profile": {...}, "profileToken": {_AuthLoginFactoryProfileToken} }
    profile: dict  # TODO - create a ProfileFactory
    profileToken: _AuthLoginFactoryProfileToken

    _errors = {
        2: "Incorrect login",
        3: "Incorrect password",
    }
    _exception = AnixartAuthError

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            code=data["code"],
            profile=data.get("profile", {}),
            profileToken=_AuthLoginFactoryProfileToken.from_dict(data.get("profileToken", {})),
            _errors=cls._errors,
            _exception=cls._exception
        )
