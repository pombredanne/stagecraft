from __future__ import unicode_literals

from nose.tools import assert_equal
from django.contrib import messages
from django.test import RequestFactory

from django.contrib.messages.storage.cookie import CookieStorage

from stagecraft.apps.datasets.admin.data_set import _clear_most_recent_message


def test_clear_most_recent_message():
    request = _make_request_with_storage()
    messages.error(request, 'first message')
    messages.error(request, 'second message')

    storage = messages.get_messages(request)

    assert_equal(2, len(storage))
    _clear_most_recent_message(request)

    assert_equal(1, len(storage))
    assert_equal('first message', storage._loaded_messages[0].message)


def test_clear_most_recent_message_doesnt_blow_up_with_zero_messages():
    request = _make_request_with_storage()

    try:
        _clear_most_recent_message(request)
    except Exception:
        assert False, "_clear_most_recent_message(..) shouldn't fail."


def _make_request_with_storage():
    request = RequestFactory().get('/')
    request._messages = CookieStorage(request)
    return request
