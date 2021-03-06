from datetime import datetime, timedelta
from functools import wraps

from hamcrest import assert_that, equal_to, none
from httmock import urlmatch, HTTMock
from mock import patch

from django.conf import settings
from django.test import TestCase

from stagecraft.apps.datasets.models import OAuthUser
from stagecraft.apps.datasets.tests.support.test_helpers import has_header
from stagecraft.libs.authorization.http import check_permission


def govuk_signon_mock(**kwargs):
    @urlmatch(netloc=r'.*signon.*')
    def func(url, request):
        if request.headers['Authorization'] == 'Bearer correct-token':
            status_code = 200
            user = {
                "user": {
                    "email": kwargs.get("email", "foobar.lastname@gov.uk"),
                    "name": kwargs.get("name", "Foobar"),
                    "organisation_slug": kwargs.get(
                        "organisation_slug", "cabinet-office"),
                    "permissions": kwargs.get("permissions", ["signin"]),
                    "uid": "a-long-uid",
                }
            }

        else:
            status_code = 401
            user = {}

        return {'status_code': status_code, 'content': user}

    return func


def with_govuk_signon(**signon_kwargs):

    def decorator(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            use_development_users = settings.USE_DEVELOPMENT_USERS
            settings.USE_DEVELOPMENT_USERS = False
            signon_mock = HTTMock(
                govuk_signon_mock(**signon_kwargs))
            try:
                with signon_mock:
                    result = func(*args, **kwargs)
            finally:
                settings.USE_DEVELOPMENT_USERS = use_development_users
            return result
        return wrapped

    return decorator


class CheckPermissionTestCase(TestCase):

    def setUp(self):
        self.use_development_users = settings.USE_DEVELOPMENT_USERS

    def tearDown(self):
        settings.USE_DEVELOPMENT_USERS = self.use_development_users

    def test_use_development_users_gets_from_dictionary(self):
        (user, has_permission) = check_permission(
            'development-oauth-access-token', 'signin')
        assert_that(user['name'], equal_to('Some User'))
        assert_that(has_permission, equal_to(True))

    def test_user_with_permission_from_signon_returns_object_and_true(self):
        settings.USE_DEVELOPMENT_USERS = False
        with HTTMock(govuk_signon_mock()):
            (user, has_permission) = check_permission(
                'correct-token', 'signin')
        assert_that(user['name'], equal_to('Foobar'))
        assert_that(has_permission, equal_to(True))

    @patch('requests.get')
    def test_signon_with_client_id(self, get_patch):
        settings.USE_DEVELOPMENT_USERS = False

        with HTTMock(govuk_signon_mock()):
            (user, has_permission) = check_permission(
                'correct-token', 'signin')
        get_patch.assert_called_with(
            'http://signon.dev.gov.uk/user.json?client_id=clientid',
            headers={
                'Authorization': 'Bearer correct-token',
            })

    def test_user_without_permission_from_signon_returns_none_and_false(self):
        settings.USE_DEVELOPMENT_USERS = False
        with HTTMock(govuk_signon_mock()):
            (user, has_permission) = check_permission('bad-auth', 'signin')
        assert_that(user, none())
        assert_that(has_permission, equal_to(False))

    def test_user_with_permission_from_database_returns_object_and_true(self):
        settings.USE_DEVELOPMENT_USERS = False

        OAuthUser.objects.create(access_token='correct-token',
                                 uid='my-uid',
                                 email='joe@example.com',
                                 permissions=['signin'],
                                 expires_at=datetime.now() + timedelta(days=1))

        (user, has_permission) = check_permission(
            'correct-token', 'signin')

        assert_that(user['email'], equal_to('joe@example.com'))
        assert_that(has_permission, equal_to(True))

    def test_user_without_permission_from_database_returns_false(self):
        settings.USE_DEVELOPMENT_USERS = False
        OAuthUser.objects.create(access_token='correct-token',
                                 uid='my-uid',
                                 email='joe@example.com',
                                 permissions=['signin'],
                                 expires_at=datetime.now() + timedelta(days=1))

        (user, has_permission) = check_permission('correct-token', 'admin')

        assert_that(has_permission, equal_to(False))

    def test_user_from_database_should_not_be_returned_if_expired(self):
        settings.USE_DEVELOPMENT_USERS = False
        OAuthUser.objects.create(access_token='correct-token-2',
                                 uid='my-uid',
                                 email='joe@example.com',
                                 permissions=['signin'],
                                 expires_at=datetime.now() - timedelta(days=1))

        with HTTMock(govuk_signon_mock()):
            (user, has_permission) = check_permission('correct-token-2',
                                                      'admin')

        assert_that(user, none())
        assert_that(has_permission, equal_to(False))
        assert_that(OAuthUser.objects.count(), equal_to(0))

    def test_user_is_written_to_database_after_successful_auth(self):
        settings.USE_DEVELOPMENT_USERS = False

        with HTTMock(govuk_signon_mock()):
            (user, has_permission) = check_permission('correct-token',
                                                      'signin')

        assert_that(OAuthUser.objects.count(), equal_to(1))

        (user, has_permission) = check_permission('correct-token', 'signin')

        assert_that(has_permission, equal_to(True))
