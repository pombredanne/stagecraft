from __future__ import unicode_literals

import json
import requests

from django.conf import settings


class BackdropError(Exception):
    pass


def create_dataset(name, capped_size):
    """
    Connect to Backdrop and create a new collection called ``name``.
    Specify ``capped_size`` in bytes to create a capped collection, or 0 to
    create an uncapped collection.
    """
    if not isinstance(capped_size, int) or capped_size < 0:
        raise BackdropError(
            "capped_size must be 0 or a positive integer number of bytes.")

    json_request = json.dumps({'capped_size': capped_size})

    backdrop_url = '{url}/data-sets/{name}'.format(
        url=settings.BACKDROP_URL, name=name)

    auth_header = (
        'Authorization',
        'Bearer {}'.format(settings.CREATE_COLLECTION_ENDPOINT_TOKEN))
    type_header = ('content-type', 'application/json')

    try:
        response = requests.post(
            backdrop_url,
            headers=dict([type_header, auth_header]),
            data=json_request)

        response.raise_for_status()
    except Exception as e:
        raise BackdropError(repr(e))