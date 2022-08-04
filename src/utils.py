from urllib.parse import urlencode


def urljoin(*args, **kwargs):
    url = "/".join(map(lambda x: str(x).rstrip("/"), args))

    if kwargs:
        return url + "?" + urlencode(kwargs)

    return url
