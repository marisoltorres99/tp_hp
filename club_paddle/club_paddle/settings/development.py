"""Development settings"""

from club_paddle.settings.django_base import *

INSTALLED_APPS.extend(
    [
        "debug_toolbar",
    ]
)

MIDDLEWARE.extend(
    [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]
)

DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": lambda request: True,
}

DEBUG = True
