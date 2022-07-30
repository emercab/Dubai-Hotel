import os


class Configuration(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "password"
