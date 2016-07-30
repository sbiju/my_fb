from django.conf import settings


PAGINATION = getattr(settings, 'BLOG_PAGINATION', 3)
ALLOW_EMPTY = getattr(settings, 'BLOG_ALLOW_EMPTY', True)
ALLOW_FUTURE = getattr(settings, 'BLOG_ALLOW_FUTURE', True)
