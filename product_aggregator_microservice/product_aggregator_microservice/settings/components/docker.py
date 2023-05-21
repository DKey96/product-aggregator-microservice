DEBUG = False

ALLOWED_HOSTS = [".localhost", "127.0.0.1"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "puromat",
        "USER": "admin",
        "PASSWORD": "hortech",
        "HOST": 'docker inspect -f "{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}" puromat-database-1',
        "PORT": 5432,
    }
}
