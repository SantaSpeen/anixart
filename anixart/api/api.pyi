import requests

from ..auth import AnixartAuth
from ..request_handler import AnixartRequestsHandler


class AnixartUserAccount:
    def __init__(self, login, password, config_file="anixart_data.json", **kwargs):
        """
            Info:
            Anixart login class object.
            ~~~~~~~~~~~~~~~~~~~~~~~~~~~
            Usage:
            >>> user = AnixartUserAccount("login", "password", config_file="anixart_data.json")
            >>> print(user.login)
            Availible params:
            ~~~~~~~~~~~~~~~~~
            * login -> Your anixart nick
            * password -> Your anixart password
            * need_reg -> If you need new account, set True
            * mail -> Real email for registration.
            * config_file -> Patch to anixart login cache
            :param login: Your anixart nick
            :param password: Anixart password
            :param need_reg: If you need new account, set True
            :param email: Real email for registration
            :param config_file: Patch to anixart login cache
            :type login: str
            :type password: str
            :type need_reg: bool
            :type email: str
            :type config_file: str
            :return: :class:`AnixUserAccount <anixart.api.AnixUserAccount>` object
        """
        self.kwargs: dict = kwargs
        self.login: str = login
        self.password: str = password
        self.config_file: str = config_file
        self.token: str = None
        self.id: int = None
        self.session: requests.Session = requests.Session()

    def __str__(self) -> str: ...
    def get_login(self) -> str: ...
    def get_password(self) -> str: ...
    def get_token(self) -> str: ...
    def get_id(self) -> int: ...

class AnixartAPI:
    def __init__(self, user: AnixartUserAccount):
        """
            Info:
            Anixart API class object.
            ~~~~~~~~~~~~~~~~~~~~~~~~~
            Usage:
            >>> user = AnixartUserAccount("login", "password", config_file="anixart_data.json")
            >>> anix = AnixartAPI(user)
            :param user: :class:`AnixUserAccount <anixart.api.AnixUserAccount>` object
            :return: :class:`AnixAPIRequests <anixart.api.AnixAPIRequests>` object
        """
        self.auth = AnixartAuth(user)
        self.user = user
        self.http_handler = AnixartRequestsHandler(user.token, user.session)
    def __str__(self) -> str: ...
    def execute(self, http_method: str, endpoint: str) -> requests.Request: ...
