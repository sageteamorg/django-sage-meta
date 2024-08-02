from .category import CategoryAdmin
from .comment import CommentAdmin
from .insight import InsightAdmin
from .media import MediaAdmin
from .instagram_account import InstagramAccountAdmin
from .page import FacebookPageDataAdmin
from .post_publish import PostPublishAdmin
from .settings import SettingsAdmin
from .story_publish import StoryPublisherAdmin
from .story import StoryAdmin
from .user import UserDataAdmin
__all__ = [
    "CategoryAdmin",
    "CommentAdmin",
    "MediaAdmin",
    "InsightAdmin",
    "StoryPublisherAdmin",
    "UserDataAdmin",
    "SettingsAdmin",
    "StoryAdmin",
    "InstagramAccountAdmin",
    "FacebookPageDataAdmin",
    "PostPublishAdmin",
]
