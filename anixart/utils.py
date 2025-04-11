# -*- coding: utf-8 -*-
from dataclasses import dataclass, field
from typing import Literal, Any

from anixart.exceptions import AnixartAPIError


@dataclass
class BaseParseFactory:
    code: int

    _errors: dict[int, str]
    _exception: type[AnixartAPIError]

    def raise_if_error(self):
        if self.code != 0:
            error = self._errors.get(self.code)
            if error:
                raise error
            else:
                raise ValueError(f"Unknown error code: {self.code}")

    @classmethod
    def from_dict(cls, data: dict) -> "BaseParseFactory":
        return cls(
            code=data.get("code", 0),
            _errors={},
            _exception=AnixartAPIError,
        )


@dataclass
class Endpoint:
    path: str
    method: Literal["GET", "POST"]
    parse_factory: type[BaseParseFactory]
    required_args: dict[str, type] = field(default_factory=dict)
    required_kwargs: dict[str, type] = field(default_factory=dict)


    _json = False
    _API_ENDPOINT = "https://api.anixart.tv/"

    def __post_init__(self):
        if self.method not in ["GET", "POST"]:
            raise ValueError("Method must be either GET or POST.")
        if not isinstance(self.required_kwargs, dict):
            raise ValueError("Required arguments must be a dictionary.")
        if not all(isinstance(v, type) for v in self.required_kwargs.values()):
            raise ValueError("All values in required arguments must be types.")

    @property
    def is_get(self) -> bool:
        return self.method == "GET"

    @property
    def is_post(self) -> bool:
        return self.method == "POST"

    @property
    def is_json(self) -> bool:
        return self._json

    def _post(self, method: str, **kwargs):
        headers = {}
        url = self._API_ENDPOINT + method
        if token:=kwargs.get("token"):
            kwargs["token"] = token
            url += f"?token={token}"

        req_settings = {"url": url}
        if self._json:
            headers["Content-Type"] = "application/json; charset=UTF-8"
            req_settings.update({"json": kwargs})
        else:
            req_settings.update({"data": kwargs})
        return req_settings, headers

    def _get(self, method: str, **kwargs):
        headers = {}
        url = self._API_ENDPOINT + method
        if token:=kwargs.get("token"):
            kwargs["token"] = token
        req_settings = {"url": url, "params": kwargs}
        return req_settings, headers

    def _check_arguments(self, **kwargs):
        """Check if all required arguments are present."""
        missing_args = []  # (arg, reason)
        for arg, arg_type in self.required_args.items():
            if arg not in kwargs:
                missing_args.append((arg, "arg missing"))
            elif not isinstance(kwargs[arg], arg_type):
                missing_args.append((arg, f"arg invalid type: {type(kwargs[arg])}"))
        for arg, arg_type in self.required_kwargs.items():
            if arg not in kwargs:
                missing_args.append((arg, "kwarg missing"))
            elif not isinstance(kwargs[arg], arg_type):
                missing_args.append((arg, f"kwarg invalid type: {type(kwargs[arg])}"))
        if missing_args:
            pretty_args = ", ".join(f"{arg} ({reason})" for arg, reason in missing_args)
            raise ValueError(f"Missing or invalid arguments: {pretty_args}")

    def build_request(self, **kwargs) -> None | tuple[dict[str, dict[str, Any] | str], dict[Any, Any]] | tuple[
        dict[str, dict[str, Any] | str], dict[str, str]]:
        """
        Build the request for the endpoint.
        :param kwargs: Arguments to be passed to the endpoint.
        :return: A tuple containing the HTTP method, headers, and request settings.
        """
        self._check_arguments(**kwargs)
        args = {arg: kwargs[arg] for arg in self.required_args}
        if self.method == "POST":
            return self._post(self.path.format(**args), **kwargs)
        if self.method == "GET":
            return self._get(self.path.format(**args), **kwargs)


def endpoint(path: str, method: Literal["GET", "POST"], parse_factory: type[BaseParseFactory], required_args: dict[str, type], required_kwargs: dict[str, type]) -> Endpoint:
    return Endpoint(path, method, parse_factory, required_args, required_kwargs)



# ----------- #  COLLECTION  # ----------- #

# GET
COLLECTION = "/collection/{}"  # collection id
COLLECTION_RELEASES = "/collection/{}/releases/{}"  # collection id / page
COLLECTION_LIST = "/collection/all/{}"  # page

COLLECTION_COMMENTS = "/collection/comment/all/{}/{}"  # collection id / page
COLLECTION_COMMENTS_VOTE = "/collection/comment/vote/{}/{}"  # collection comment id / mark (1, 2)
COLLECTION_COMMENTS_VOTES = "/collection/comment/votes/{}/{}"  # collection comment id / page
COLLECTION_COMMENTS_DELETE = "/collection/comment/delete/{}"  # collection comment id

COLLECTION_FAVORITE = "/collectionFavorite/all/{}"  # page
COLLECTION_FAVORITE_ADD = "/collectionFavorite/add/{}"  # collection id
COLLECTION_FAVORITE_DELETE = "/collectionFavorite/delete/{}"  # collection id

# POST
COLLECTION_COMMENTS_ADD = "/collection/comment/add/{}"  # collection id
COLLECTION_COMMENTS_EDIT = "/collection/comment/edit/{}"  # collection comment id
COLLECTION_COMMENTS_REPLIES = "/collection/comment/replies/{}/{}"  # collection comment id / page

# Not Checked
# GET
COLLECTION_PROFILE = "/collection/all/profile/{}/{}"  # p_id/page
COLLECTION_RELEASE_IN = "/collection/all/release/{}/{}"  # r_id/page

COLLECTION_MY = "/collectionMy/{id}/releases"
COLLECTION_MY_DELETE = "/collectionMy/delete/{}"  # collectionId
COLLECTION_MY_ADD_RELEASE = "/collectionMy/release/add/{}"  # collectionId

# POST
COLLECTION_COMMENTS_PROCESS = "/collection/comment/process/{}"  # commentId
COLLECTION_COMMENTS_REPORT = "/collection/comment/report/{}"  # commentId

COLLECTION_REPORT = "/collection/report/{}"  # collectionId

COLLECTION_MY_CREATE = "/collectionMy/create"
COLLECTION_MY_EDIT = "/collectionMy/edit/{}"  # collectionId
COLLECTION_MY_EDIT_IMAGE = "/collectionMy/editImage/{}"  # collectionId

# ----------- #    RELEASE    # ----------- #

# GET
RELEASE = "/release/{}"  # release id
RELEASE_VOTE_ADD = "/release/vote/add/{}/{}"  # release id / mark 1-5
RELEASE_VOTE_DELETE = "/release/vote/delete/{}"  # release id
RELEASE_RANDOM = "/release/random"

RELEASE_COMMENTS = "/release/comment/all/{}/{}"  # release id / page
RELEASE_COMMENTS_VOTE = "/release/comment/vote/{}/{}"  # release comment id / mark (1, 2)
RELEASE_COMMENTS_VOTES = "/release/comment/votes/{}/{}"  # release comment id / page
RELEASE_COMMENTS_REPLIES = "/release/comment/replies/{}/{}"  # release comment id / page
RELEASE_COMMENTS_DELETE = "/release/comment/delete/{}"  # release comment id

# POST
RELEASE_COMMENTS_ADD = "/release/comment/add/{}"  # release id
RELEASE_COMMENTS_EDIT = "/release/comment/edit/{}"  # release comment id

# Not Checked
# GET
RELEASE_COMMENTS_REPORT = "/release/comment/report/{}"  # commentId
RELEASE_COMMENTS_PROCESS = "/release/comment/process/{}"  # commentId

RELEASE_PROFILE_COMMENTS = "/release/comment/all/profile/{}/{}"  # p_id/page

RELEASE_STREAMING_PLATFORM = "/release/streaming/platform/{}/"  # releaseId

# POST
RELEASE_REPORT = "/release/report/{}"  # r_id

# ----------- #    OTHER    # ----------- #
# TODO OTHER: EXPORT_BOOKMARKS, IMPORT_BOOKMARKS, CAN_IMPORT_BOOKMARKS

# GET
TYPE = "/type/all"
TYPE_RELEASE = "/type/{}"  # r_id
TOGGLES = "/config/toggles?version_code={}&is_beta={}"  # version_code: int, is_beta: bool
SCHEDULE = "/schedule"

# POST
# {"bookmarksExportProfileLists":[0 - favorite, + all in AnixList]}
EXPORT_BOOKMARKS = "/export/bookmarks"
# {"completed":[],"dropped":[],"holdOn":[],"plans":[],"watching":[],"selected_importer_name":"Shikimori"}
IMPORT_BOOKMARKS = "/import/bookmarks"
CAN_IMPORT_BOOKMARKS = "/import/status"  # code: 0 - Yes, code: 2 - no

# Not Checked
# GET
# page {token, genres: [], studio, category, status, year, episodes, sort,
# country, season, duration, ratings: [], extended_mode: bool}
FILTER = "/filter/{}"
RELATED = "related/{}/{}"  # relatedId/page

# POST
VIDEO_PARSE = "/video/parse"

# ----------- #    SEARCH    # ----------- #
# TODO SEARCH: *

# { "query": text, "searchBy": 0}
# POST
SEARCH_COLLECTION = "/search/collections/{}"  # page
SEARCH_RELEASE = "/search/releases/{}"  # page
SEARCH_FAVORITE = "/search/favorites/{}"  # page
SEARCH_COLLECTION_FAVORITE = "/search/favoriteCollections/{}"  # page
SEARCH_LIST = "/search/profile/list/{}/{}"  # list id / page
SEARCH_PROFILE = "/search/profiles/{}"  # page
SEARCH_HISTORY = "/search/history/{}"  # page

#
SEARCH_COLLECTION_PROFILE = "/search/profileCollections/{}/{}"  # p_id/page

# ----------- #    NOTIFICATIONS    # ----------- #
# TODO NOTIFICATIONS: *

# GET
NOTIFICATION_READ = "/notification/read"
NOTIFICATION_COUNT = "/notification/count"
NOTIFICATION_COLLECTION_COMMENTS = "/notification/collectionComments/{}"  # page
NOTIFICATION_MY_COLLECTION_COMMENTS = "/notification/my/collection/comments/{}"  # page
NOTIFICATION_RELEASE_COMMENTS = "/notification/releaseComments/{}"  # page
NOTIFICATION_EPISODES = "/notification/episodes/{}"  # page
NOTIFICATION_FRIEND = "/notification/friends/{}"  # page

NOTIFICATION_COLLECTION_COMMENTS_DELETE = "/notification/collectionComment/delete/{}"  # n_id
NOTIFICATION_MY_COLLECTION_COMMENTS_DELETE = "/notification/my/collection/comment/delete/{}"  # page
NOTIFICATION_RELEASE_COMMENTS_DELETE = "/notification/releaseComment/delete/{}"  # page
NOTIFICATION_EPISODES_DELETE = "/notification/episode/delete/{}"  # page
NOTIFICATION_FRIEND_DELETE = "/notification/friends/delete/{}"  # page

# ----------- #    DISCOVER   # ----------- #
# TODO DISCOVER: *

# Not Checked
# POST
DISCOVER_COMMENTS = "/discover/comments"
DISCOVER_DISCUSSING = "/discover/discussing"  # {token}
DISCOVER_INTERESTING = "/discover/interesting"
DISCOVER_RECOMMENDATION = "/discover/recommendations/{}"  # page
DISCOVER_WATCHING = "/discover/watching/{}"  # page

# ----------- #    EpisodeApi.kt    # ----------- #
# TODO EpisodeApi.kt: *

# Здесь методы из com.swiftsoft.anixartd.network.api.EpisodeApi.kt
# Если надо, переделай так как тебе надо

# Not Checked
# GET
# @GET("episode/target/{releaseId}/{sourceId}/{position}")
# @GET("episode/{releaseId}/{typeId}/{sourceId}")
# @GET("episode/{releaseId}")
# @GET("episode/updates/{releaseId}/{page}")

# POST
# @POST("episode/report/{releaseId}/{sourceId}/{position}")
# @POST("episode/unwatch/{releaseId}/{sourceId}/{position}")
# @POST("episode/unwatch/{releaseId}/{sourceId}")
# @POST("episode/watch/{releaseId}/{sourceId}/{position}")
# @POST("episode/watch/{releaseId}/{sourceId}")

# ----------- #    FAVORITE    # ----------- #
# TODO FAVORITE: *

# Not Checked
# GET
FAVORITE = "/favorite/all/{}"  # r_id
FAVORITE_ADD = "/favorite/add/{}"  # r_id
FAVORITE_DELETE = "/favorite/delete/{}"  # r_id {sort}

# ----------- #    HISTORY    # ----------- #
# TODO HISTORY: *

# GET
HISTORY = "/history/{}"  # page

# Not Checked
# GET
HISTORY_ADD = "/history/add/{}/{}/{}"  # r_id/s_id/position
HISTORY_DELETE = "/history/delete/{}"  # r_id
