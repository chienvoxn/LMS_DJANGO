from django.conf import settings


def rag_setting(name, default=None):
    return getattr(settings, name, default)
