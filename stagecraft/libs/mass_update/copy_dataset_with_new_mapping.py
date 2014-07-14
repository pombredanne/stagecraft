#from __future__ import unicode_literals

#import pprint as pp
#import random
#import json
#from performanceplatform.client import DataSet as client
#BEARER_TOKEN_LENGTH = 64
#from stagecraft.apps.datasets.models import DataGroup, DataSet, DataType
#import reversion


class CopyDatasetWithNewMapping(object):
    pass

    #base_url = 'https://www.preview.performance.service.gov.uk'

    #input_sets = [
        #'carers_allowance_monthly_claims',
        #'carers_allowance_weekly_claims'
    #]

    #output_set = 'carers_allowance_transactions_by_channel'

    #key_mapping = {
        #"key": "channel",
        #"value": "count"
    #}

    #value_mapping = {
        #"ca_clerical_received": "paper",
        #"ca_e_claims_received": "digital"
    #}


    #def _get_output_data_set(token=None):
        #data_set = client.from_name(base_url, output_set)
        #if token is not None:
            #data_set.set_token(token)
        #else:
            #data_set.set_token(settings.STAGECRAFT_DATA_SET_QUERY_TOKEN)
        #return data_set


    #def _generate_bearer_token():
        #"""
        #>>> len(_generate_bearer_token()) == BEARER_TOKEN_LENGTH
        #True
        #>>> import re
        #>>> regex = re.compile("^[(a|b|c|d|e|f|g|h|j|k|m|n|p|q|r|s|t|u|v|w|x|y|z|2|3|4|5|6|7|8|9)]{10,}$")
        #>>> type(regex.match(_generate_bearer_token()))
        #<type '_sre.SRE_Match'>
        #"""
        #chars = "abcdefghjkmnpqrstuvwxyz23456789"
        #token = "".join(random.choice(chars) for _ in range(BEARER_TOKEN_LENGTH))
        #return token


    #def get_data_from_claims_sets():
        #input_data = []
        #for set_name in input_sets:
            #data_set = client.from_name(base_url, set_name)
            #for item in data_set.get().json()['data']:
                #input_data.append(item)
        #return input_data


    #def apply_new_key_mappings(document):
        #for key, val in document.items():
            #if key in key_mapping:
                #document.pop(key)
                #document[key_mapping[key]] = val
            #else:
                #document[key] = val
        #return document


    #def apply_new_values(document):
        #for key, val in document.items():
            #if val in value_mapping:
                #document['comment'] = str(document['comment']) + " / " + val
                #document[key] = value_mapping[val]
        #return document


    #def build_documents(documents):
        #docs = []
        #for document in documents:
            #doc = apply_new_values(apply_new_key_mappings(document))
            #docs.append(doc)
        #return docs


    #def post_docs_to_production(documents):
        #data_set = _get_output_data_set()
        #data_set.post(documents)


    #def clear_docs_from_output_set():
        #data_set = _get_output_data_set()
        #data_set.empty_data_set()


    #def get_or_create_carers_transactions_by_channel(orm):
        #try:
            #return orm['datasets.DataSet'].objects.get(
                #name=output_set
            #)
        #except orm['datasets.DataSet'].DoesNotExist:
            #by_transaction = orm['datasets.DataSet'].objects.create(
                #name=output_set,
                #data_group='carers-allowance',
                #data_type='transactions-by-channel',
                #bearer_token=_generate_bearer_token(),
                #upload_format='excel',
                #upload_filters='backdrop.core.upload.filters.first_sheet_filter',
                #max_age_expected=2678400,
                #published=True
            #)
            #return by_transaction

    #def map_one_to_one_fields(mapping, pairs):
        #"""
        #>>> mapping = {'a': 'b'}
        #>>> pairs = {'a': 1}
        #>>> map_one_to_one_fields(mapping, pairs)
        #{'b': 1}
        #>>> mapping = {'a': ['b', 'a']}
        #>>> map_one_to_one_fields(mapping, pairs)
        #{'a': 1, 'b': 1}
        #"""
        #mapped_pairs = dict()
        #for key, value in pairs.items():
            #if key in mapping:
                #targets = mapping[key]
                #if not isinstance(targets, list):
                    #targets = list(targets)
                #for target in targets:
                    #mapped_pairs[target] = value
            #else:
                #mapped_pairs[key] = value

        #return mapped_pairs

    #def apply_mapping(mapping, pairs):
        #logging.warn("{} -- {}".format(mapping, pairs))
        #return dict(map_one_to_one_fields(mapping, pairs).items())
