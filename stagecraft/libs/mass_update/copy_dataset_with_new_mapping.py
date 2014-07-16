import reversion
from performanceplatform.client import DataSet as client
from stagecraft.apps.datasets.models import DataGroup, DataSet, DataType
from django.conf import settings


#should be in model? should be imported differently (not in init)?
#should pass in whole mapping?
@reversion.create_revision()
def migrate_data_set(old_name, changed_attributes, data_mapping):
    #refactor to use group and type not names
    existing_data_set = get_existing_data_set(old_name)
    new_data_set_attributes = get_new_attributes(existing_data_set.serialize(), changed_attributes)
    new_data_set = get_or_create_new_data_set(new_data_set_attributes)
    old_data = get_old_data(old_name)
    new_data = convert_old_data(old_data, data_mapping)
    post_new_data(new_data_set.name, new_data)

def get_existing_data_set(old_name):
    return DataSet.objects.get(name=old_name)

def get_new_attributes(existing_attributes, changed_attributes):
    """
    >>> existing_attributes = {'a': 1, 'b': 2, 'c': 3}
    >>> changed_attributes = {'a': 6, 'c': 'x,y'}
    >>> get_new_attributes(existing_attributes, changed_attributes)
    {'a': 6, 'c': 'x,y', 'b': 2}
    """
    return dict(existing_attributes.items() + changed_attributes.items())

def get_or_create_new_data_set(new_attributes):
    (data_type, new) = DataType.objects.get_or_create(name=new_attributes.pop('data_type'))
    (data_group, new) = DataGroup.objects.get_or_create(name=new_attributes.pop('data_group'))
    (obj, new) = DataSet.objects.get_or_create(data_type=data_type, data_group=data_group)
    new_attributes['data_type'] = data_type
    new_attributes['data_group'] = data_group
    del new_attributes['schema']
    del new_attributes['name']
    data_set_to_update_queryset = DataSet.objects.filter(name=obj.name)
    data_set_to_update_queryset.update(**new_attributes)
    return data_set_to_update_queryset.first()


def get_old_data(old_data_set_name):
    base_url = settings.BACKDROP_URL
    data_set_client = client.from_name(base_url, old_data_set_name)
    return data_set_client.get().json()['data']


def apply_new_key_mappings(document, key_mapping):
    for key, val in document.items():
        if key in key_mapping:
            document.pop(key)
            document[key_mapping[key]] = val
        else:
            document[key] = val
    return document


def apply_new_values(document, value_mapping):
    for key, val in document.items():
        if val in value_mapping:
            document[key] = value_mapping[val]
    return document


def convert_old_data(old_data, data_mapping):
    new_data = []
    key_mapping = data_mapping['key_mapping']
    value_mapping = data_mapping['value_mapping']
    for document in old_data:
        doc = apply_new_values(apply_new_key_mappings(document, key_mapping), value_mapping)
        new_data.append(doc)

    return new_data


def post_new_data(data_set_name, data):
    base_url = settings.BACKDROP_URL
    data_set_client = client.from_name(base_url, data_set_name)
    return data_set_client.post(data)
