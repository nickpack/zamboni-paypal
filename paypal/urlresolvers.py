from threading import local
from django.conf import settings
from django.core import urlresolvers

django_reverse = urlresolvers.reverse


# Thread-local storage for URL prefixes.  Access with {get,set}_url_prefix.
_local = local()

def get_url_prefix():
    """Get the prefix for the current thread, or None."""
    return getattr(_local, 'prefix', None)

def reverse(viewname, urlconf=None, args=None, kwargs=None, prefix=None,
            current_app=None, add_prefix=True):
    """Wraps django's reverse to prepend the correct locale and app."""
    prefixer = get_url_prefix()
    if settings.MARKETPLACE and settings.REGION_STORES:
        prefix = None
        # Blank out the script prefix since we add that in prefixer.fix().
    if prefixer:
        prefix = prefix or '/'
    url = django_reverse(viewname, urlconf, args, kwargs, prefix, current_app)
    if prefixer and add_prefix:
        return prefixer.fix(url)
    else:
        return url