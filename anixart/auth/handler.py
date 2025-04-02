import json
import logging
import os.path

from .endpoints import SING_IN, CHANGE_PASSWORD, PROFILE
from .exceptions import AnixartAuthError
from .request_handler import AnixartRequestsHandler


def _parse_response(data):
    ready = data.json()
    ready.update({"status_code": data.status_code})
    code = ready['code']
    if code != 0:
        if code == 2:
            raise AnixartAuthError("Incorrect login.")
        if code == 3:
            raise AnixartAuthError("Incorrect password.")
        print("\n\n" + data.text + "\n\n")
        raise AnixartAuthError("Unknown auth error.")
    return ready


class AnixartAuth(AnixartRequestsHandler):

    def __init__(self, user):
        super(AnixartAuth, self).__init__(None, user.session, "anixart.auth.AnixAuth")
        self.user = user
        self.filename = user.config_file

    def _save_config(self, data):
        with open(self.filename, "w") as f:
            json.dump(data, f)
        return data

    def _open_config(self):
        if os.path.isfile(self.filename):
            with open(self.filename, "r") as read_file:
                data = json.load(read_file)
            return data
        else:
            return None

    def sing_in(self):
        config = self._open_config()
        if config:
            uid = config.get("id")
            token = config.get("token")
            if not self.get(PROFILE.format(uid), {"token": token}).json().get("is_my_profile") or \
                    self.user.__login != config.get("login"):
                logging.getLogger("anixart.api.AnixAPI").debug("Invalid config file. Re login.")
            else:
                self.user.id = uid
                self.user.__token = token
                return config
        payload = {"login": self.user.__login, "password": self.user.__password}
        res = self.post(SING_IN, payload)
        ready = _parse_response(res)
        uid = ready["profile"]["id"]
        token = ready["profileToken"]["token"]
        self.user.id = uid
        self.user.__token = token
        self._save_config({"id": uid, "token": token, "login": self.user.__login})
        return ready

    def change_password(self, old, new):
        return self.get(CHANGE_PASSWORD, {"current": old, "new": new, "token": self.user.token})
