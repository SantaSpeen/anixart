from dataclasses import dataclass

@dataclass
class ProfileHistory:
    # TODO: Надо ещё изучить релизы
    pass

@dataclass
class ProfileVote:
    # TODO: Надо ещё изучить релизы
    pass

@dataclass
class ProfileRoles:
    # TODO: Надо ещё изучить роли (У меня их нет(()
    pass

@dataclass
class Profile:
    id: int
    login: str
    avatar: str

@dataclass
class ProfileFriendsPreview(Profile):
    friend_count: int
    friend_status: int
    is_sponsor: bool
    is_online: bool
    is_verified: bool
    is_social: bool
    badge_id: None
    badge_name: None
    badge_type: None
    badge_url: None

@dataclass
class ProfileFull(Profile):
    status: str
    rating_score: int
    history: list[ProfileHistory]
    votes: list[ProfileVote]
    roles: list[ProfileRoles]
    friends_preview: list[ProfileFriendsPreview]
    collections_preview: list  # TODO: Коллекции изучить
    release_comments_preview: list  # Тут вообще не понял
    comments_preview: list # Тут типа превью к коментам
    release_videos_preview: list # Тут вообще не понял
    watch_dynamics: list # Тут вообще не понял
    last_activity_time: int
    register_date: int
    vk_page: str
    tg_page: str
    inst_page: str
    tt_page: str
    discord_page: str
    ban_expires: int
    ban_reason: str
    privilege_level: int
    watching_count: int
    plan_count: int
    completed_count: int
    hold_on_count: int
    dropped_count: int
    favorite_count: int
    comment_count: int
    collection_count: int
    video_count: int
    friend_count: int
    subscription_count: int
    watched_episode_count: int
    watched_time: int
    sponsorshipExpires: int
    is_private: bool
    is_sponsor: bool
    is_banned: bool
    is_perm_banned: bool
    is_bookmarks_transferred: bool
    is_sponsor_transferred: bool
    is_vk_bound: bool
    is_google_bound: bool
    is_release_type_notifications_enabled: bool
    is_episode_notifications_enabled: bool
    is_first_episode_notification_enabled: bool
    is_related_release_notifications_enabled: bool
    is_report_process_notifications_enabled: bool
    is_comment_notifications_enabled: bool
    is_my_collection_comment_notifications_enabled: bool
    is_my_article_comment_notifications_enabled: bool
    is_verified: bool
    is_blocked: bool
    is_me_blocked: bool
    is_stats_hidden: bool
    is_counts_hidden: bool
    is_social_hidden: bool
    is_friend_requests_disallowed: bool
    is_online: bool
    badge: None
    friend_status: None

    is_my_profile: bool = False

    @classmethod
    def from_response(cls, response: dict) -> "Profile":
        profile = {"is_my_profile": response['is_my_profile'], **response['profile']}
        return cls(**profile)

class _login:
    pos_id: int
    id: int
    newLogin: str
    timestamp: int

class ProfileLoginsHistory:
    content: list[_login]
    total_count: int
    # total_page_count: int
    # current_page: int


# From singup
#     "profile": {
#         "id": 123,
#         "login": "loginstr",
#         "avatar": "*.jpg",
#         "status": "123",
#         "badge": null,
#         "history": [],
#         "votes": [],
#         "roles": [],
#         "last_activity_time": 100046000,
#         "register_date": 100046000,
#         "vk_page": "",
#         "tg_page": "",
#         "inst_page": "",
#         "tt_page": "",
#         "discord_page": "",
#         "ban_expires": 0,
#         "ban_reason": null,
#         "privilege_level": 0,
#         "watching_count": 1,
#         "plan_count": 1,
#         "completed_count": 1,
#         "hold_on_count": 1,
#         "dropped_count": 1,
#         "favorite_count": 1,
#         "comment_count": 1,
#         "collection_count": 0,
#         "video_count": 0,
#         "friend_count": 1,
#         "subscription_count": 0,
#         "watched_episode_count": 1,
#         "watched_time": 1,
#         "is_private": false,
#         "is_sponsor": false,
#         "is_banned": false,
#         "is_perm_banned": false,
#         "is_bookmarks_transferred": false,
#         "is_sponsor_transferred": false,
#         "is_vk_bound": true,
#         "is_google_bound": true,
#         "is_release_type_notifications_enabled": false,
#         "is_episode_notifications_enabled": true,
#         "is_first_episode_notification_enabled": true,
#         "is_related_release_notifications_enabled": true,
#         "is_report_process_notifications_enabled": true,
#         "is_comment_notifications_enabled": true,
#         "is_my_collection_comment_notifications_enabled": true,
#         "is_my_article_comment_notifications_enabled": false,
#         "is_verified": false,
#         "friends_preview": [],
#         "collections_preview": [],
#         "release_comments_preview": [],
#         "comments_preview": [],
#         "release_videos_preview": [],
#         "watch_dynamics": [],
#         "friend_status": null,
#         "rating_score": 0,
#         "is_blocked": false,
#         "is_me_blocked": false,
#         "is_stats_hidden": false,
#         "is_counts_hidden": false,
#         "is_social_hidden": false,
#         "is_friend_requests_disallowed": false,
#         "is_online": false,
#         "sponsorshipExpires": 0
#     }