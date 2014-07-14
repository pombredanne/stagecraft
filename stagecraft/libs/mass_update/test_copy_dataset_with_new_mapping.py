import mock
from stagecraft.apps.datasets.models import DataGroup, DataSet, DataType
from stagecraft.libs.backdrop_client import disable_backdrop_connection
from stagecraft.libs.purge_varnish import disable_purge_varnish
from django.test import TestCase
from stagecraft.libs.mass_update import CopyDatasetWithNewMapping
from nose.tools import assert_equal


class TestDataSetMassUpdate(TestCase):
    data_set_mapping = {
            #use real name?
            'old_name': "some_name",
            #use real attrs?
            'new_data_set': {
                    'some_attribute': "a",
                    'name': "b"
                },
            'data_mapping': {
                    'key_mapping': {
                            "key": "channel",
                            "value": "count"
                        },
                    'value_mapping': {
                            "ca_clerical_received": "paper",
                            "ca_e_claims_received": "digital"
                        }
                }
        }

    #real new data set?
    #real find data set?
    #stub get data
    #stub post data
    def test_correct_new_data_set_created(self):
        migrate_data_set(mapping['old_name'], mapping['new_data_set'], mapping["data_mapping"])

    #real new data set?
    #real find data set?
    #stub get data
    #stub post data
    def test_handles_new_data_set_already_exists(self):
        pass

    #real new data set?
    #real find data set?
    #stub get data
    #stub post data
    def test_correct_data_posted_to_new_data_set_given_response(self):
        pass


    #def forwards(self, orm):
        ##non destructive - the old ones hang around in case there is a problem
        ##and we need to roll back.
        #for mapping in transaction_by_channel_data_set_mappings:
            #migrate_data_set(mapping['old_name'], mapping['new_data_set'], mapping["data_mapping"])
