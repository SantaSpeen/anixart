from anixart.utils import endpoint

# # ----------- # PROFILE # ----------- #
# # TODO PROFILE: SETTINGS, SETTINGS_RELEASE, SETTINGS_RELEASE_FIRST,
# #  SETTINGS_COMMENTS, SETTINGS_COLLECTION, EDIT_AVATAR, SETTINGS_RELEASE_LIST,
# #  SETTINGS_RELEASE_TYPE
#
# # GET
# PROFILE = "/profile/{}"  # + profile id  (Токен нужен только что бы был is_my_profile)
# PROFILE_NICK_HISTORY = "/profile/login/history/all/{}/{}"  # profile id / page  (Токен не нужен)
#
# PROFILE_BLACKLIST = "/profile/blocklist/all/{}"  # page
# PROFILE_BLACKLIST_ADD = "/profile/blocklist/add/{}"  # profile id
# PROFILE_BLACKLIST_REMOVE = "/profile/blocklist/remove/{}"  # profile id
#
# FRIENDS = "/profile/friend/all/{}/{}"  # profile id / page
# FRIENDS_RQ_IN = "/profile/friend/requests/in/{}"  # page
# FRIENDS_RQ_OUT = "/profile/friend/requests/out/{}"  # page
# FRIENDS_RQ_IN_LAST = "/profile/friend/requests/in/last"
# FRIENDS_RQ_OUT_LAST = "/profile/friend/requests/out/last"
# FRIENDS_SEND = "/profile/friend/request/send/{}"  # profile id
# FRIENDS_REMOVE = "/profile/friend/request/remove/{}"  # profile id
#
# VOTE_VOTED = "/profile/vote/release/voted/{}/{}"  # profile id / page
# # Да, ребята из аниксарта не знают английский; ↓
# # noinspection SpellCheckingInspection
# VOTE_UNVENTED = "/profile/vote/release/unvoted/{}"  # page
#
# LISTS = "/profile/list/all/{}/{}/{}"  # profile id / list id / page
#
# SETTINGS_NOTIFICATION = "/profile/preference/notification/my"
# SETTINGS_NOTIFICATION_RELEASE = "/profile/preference/notification/episode/edit"
# SETTINGS_NOTIFICATION_RELEASE_FIRST = "/profile/preference/notification/episode/first/edit"
# SETTINGS_NOTIFICATION_COMMENTS = "/profile/preference/notification/comment/edit"
# SETTINGS_NOTIFICATION_COLLECTION = "/profile/preference/notification/my/collection/comment/edit"
#
# CHANGE_PASSWORD = "/profile/preference/password/change"
#
# # POST
# EDIT_STATUS = "/profile/preference/status/edit"
# EDIT_SOCIAL = "/profile/preference/social/edit"
# EDIT_AVATAR = "/profile/preference/avatar/edit"
#
# # {"profileStatusNotificationPreferences":[0 - favorite, + all in AnixList]}
# SETTINGS_NOTIFICATION_RELEASE_LIST = "/profile/preference/notification/status/edit"
# # {"profileTypeNotificationPreferences":[type ids]}
# SETTINGS_NOTIFICATION_RELEASE_TYPE = "/profile/preference/notification/type/edit"
#
# # Not Checked
# # GET
# PROFILE_SOCIAL = "/profile/social/{}"  # profile id
#
# FRIENDS_RECOMMENDATION = "/profile/friend/recommendations"
# FRIENDS_RQ_HIDE = "profile/friend/request/hide/{}"  # profile id
#
# SETTINGS_PROFILE = "/profile/preference/my"
# SETTINGS_PROFILE_CHANGE_EMAIL = "/profile/preference/email/change"  # {current_password, current, new}
# SETTINGS_PROFILE_CHANGE_EMAIL_CONFIRM = "/profile/preference/email/change/confirm"  # {current}
#
# # /profile/preference/social
# SETTINGS_PROFILE_STATUS_DELETE = "/profile/preference/status/delete"
#
# # POST
# PROFILE_PROCESS = "/profile/process/{}"  # profile id
#
# SETTINGS_PROFILE_CHANGE_LOGIN = "/profile/preference/email/login/confirm"  # {login}
# SETTINGS_PROFILE_CHANGE_LOGIN_INFO = "/profile/preference/email/login/info"  # {login}
#
# SETTINGS_PROFILE_BIND_GOOGLE = "/profile/preference/google/bind"  # {idToken, }
# SETTINGS_PROFILE_UNBIND_GOOGLE = "/profile/preference/google/unbind"
# SETTINGS_PROFILE_BIND_VK = "/profile/preference/google/bind"  # {accessToken, }
# SETTINGS_PROFILE_UNBIND_VK = "/profile/preference/google/unbind"
#
# SETTINGS_PROFILE_PRIVACY_COUNTS = "/profile/preference/privacy/counts/edit"
# SETTINGS_PROFILE_PRIVACY_FRIENDS_REQUESTS = "/profile/preference/privacy/friendRequests/edit"
# SETTINGS_PROFILE_PRIVACY_SOCIAL = "/profile/preference/privacy/social/edit"
# SETTINGS_PROFILE_PRIVACY_STATS = "/profile/preference/privacy/stats/edit"

class AnixartProfileEndpoints:
    profile = endpoint("/profile/{id}", "GET", None, {"id": int}, {})
