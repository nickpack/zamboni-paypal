from urllib import urlencode
from django.conf import settings
import urlparse
from django.utils.encoding import smart_str

def absolutify(url, site=None):
    """Takes a URL and prepends the SITE_URL"""
    if url.startswith('http'):
        return url
    else:
        if site:
            return site + url
        return settings.SITE_URL + url

def urlparams(url_, hash=None, **query):
    """
    Add a fragment and/or query paramaters to a URL.

    New query params will be appended to exising parameters, except duplicate
    names, which will be replaced.
    """
    url = urlparse.urlparse(url_)
    fragment = hash if hash is not None else url.fragment

    # Use dict(parse_qsl) so we don't get lists of values.
    q = url.query
    query_dict = dict(urlparse.parse_qsl(smart_str(q))) if q else {}
    query_dict.update((k, v) for k, v in query.items())

    query_string = urlencode([(k, v) for k, v in query_dict.items()
                                     if v is not None])
    new = urlparse.ParseResult(url.scheme, url.netloc, url.path, url.params,
        query_string, fragment)
    return new.geturl()