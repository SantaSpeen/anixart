from anixart.utils import endpoint
from .factories import AuthLoginFactory


# ----------- #   AUTH   # ----------- #
#
# POST
# SING_UP = None
# SING_IN = "/auth/signIn"
#
# !! Not Checked !!
# POST
# AUTH_SING_IN_WITH_GOOGLE = "/auth/google"  # {googleIdToken} or {login, email, googleIdToken}
# AUTH_SING_IN_WITH_VK = "/auth/vk"  # {vkAccessToken}


class AnixartAuthEndpoints:
    """Anixart API authentication endpoints."""
    singup = None # Удалено дабы исключить автореги (по просьбе аниксарта)
    login = endpoint("/auth/signIn", "POST", AuthLoginFactory, {}, {"login": str, "password": str})

    # login_google = None # endpoint("/auth/google", "POST", {}, {"googleIdToken": str})
    # login_vk = None # endpoint("/auth/vk", "POST", {}, {"vkAccessToken": str})
