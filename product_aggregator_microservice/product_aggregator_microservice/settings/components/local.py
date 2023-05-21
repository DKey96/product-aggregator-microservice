import os

DEBUG = True

ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "NAME": "applifting",
        "ENGINE": "django.db.backends.postgresql",
        "HOST": "localhost",
        "USER": "applifting",
        "PASSWORD": "applifting",
        "DISABLE_SERVER_SIDE_CURSORS": True,
        "OPTIONS": {"application_name": os.getenv("HOSTNAME", "unknown")},
    },
}
