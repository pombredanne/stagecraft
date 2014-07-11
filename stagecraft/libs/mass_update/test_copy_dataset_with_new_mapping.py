import mock
from stagecraft.apps.datasets.models import DataGroup, DataSet, DataType
from stagecraft.libs.backdrop_client import disable_backdrop_connection
from stagecraft.libs.purge_varnish import disable_purge_varnish
from django.test import TestCase
from stagecraft.libs.mass_update import CopyDatasetWithNewMapping
from nose.tools import assert_equal


class TestDataSetMassUpdate(TestCase):
    pass
