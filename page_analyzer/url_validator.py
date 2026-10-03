from urllib.parse import urlparse

import validators


def norm_url(url):
    parsed_url = urlparse(url)
    norm_url = f"{parsed_url.scheme}://{parsed_url.hostname}"
    return norm_url


def validate_url(url):
    errors = {}

    if not validators.url(url):
        errors['url'] = 'Некорректный формат URL'
    if url == "":
        errors['url'] = 'URL не может быть пустым'
    return errors