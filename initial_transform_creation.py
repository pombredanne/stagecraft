from django.conf import settings

from stagecraft.apps.dashboards.models.dashboard import Dashboard

from stagecraft.apps.datasets.models.data_group import DataGroup
from stagecraft.apps.datasets.models.data_type import DataType
from stagecraft.apps.datasets.models.data_set import DataSet

import json
import requests

if 'development' in settings.APP_HOSTNAME:
    HTTP_PROTOCOL = 'http'
else:
    HTTP_PROTOCOL = 'https'

STAGECRAFT_ROOT = '{0}://{1}'.format(HTTP_PROTOCOL, settings.APP_HOSTNAME)

def find_modules(dashboards, module_type):
    for dashboard in dashboards:
        if dashboard.slug == 'prison-visits':
            modules = dashboard.module_set.filter(type__name=module_type)
        else:
            modules = []

        for module in modules:
            yield module

completion_transform_type = {
    "name": "rate",
    "function": "backdrop.transformers.tasks.rate.compute",
    "schema": {
        "$schema": "http://json-schema.org/draft-03/schema#",
        "type": "object",
        "properties": {
            "denominatorMatcher": {
                "type": "string",
                "required": True,
            },
            "numeratorMatcher": {
                "type": "string",
                "required": True,
            },
            "matchingAttribute": {
                "type": "string",
                "required": True,
            },
            "valueAttribute": {
                "type": "string",
                "required": True,
            }
        },
        "additionalProperties": False,
    }
}

user_satisfaction_transform_type = {
    "name": "user_satisfaction",
    "function": "backdrop.transformers.tasks.user_satisfaction.compute",
    "schema": {}
}

transform_types = [completion_transform_type, user_satisfaction_transform_type]
transform_metadata = {
    'rate': {
        'module': 'completion_rate',
        'data_type_append': 'rate',
        'options': {
            'denominatorMatcher': 'denominator-matcher',
            'numeratorMatcher': 'numerator-matcher',
            'matchingAttribute': 'matching-attribute',
            'valueAttribute': 'value-attribute',
        },
    },
    'user_satisfaction': {
        'module': 'user_satisfaction_graph',
        'data_type_append': 'weekly',
        'options': {},
    }
}

headers = {
    'Authorization': 'Bearer {0}'.format(settings.MIGRATION_SIGNON_TOKEN),
    'Content-Type': 'application/json',
}

dashboards = Dashboard.objects.all()

for transform_type in transform_types:
    r = requests.post(STAGECRAFT_ROOT + '/transform-type',
                    data=json.dumps(transform_type), headers=headers)

    if r.status_code != 200:
        print r.text
        exit('Received error from Stagecraft when making TransformType: ' + transform_type['name'])

    transform_type_id = r.json()['id']

    metadata = transform_metadata[transform_type['name']]
    for module in find_modules(dashboards, metadata['module']):
        data_group_name = module.data_set.data_group.name
        data_type_name = module.data_set.data_type.name
        new_data_type_name = data_type_name + '-' + metadata['data_type_append']

        (data_group, data_group_created) = DataGroup.objects.get_or_create(name=data_group_name)
        (data_type, data_type_created) = DataType.objects.get_or_create(name=new_data_type_name)

        if data_group_created:
            exit('Data group did not exist before script started')

        (data_set, data_set_created) = DataSet.objects.get_or_create(
            data_group=data_group,
            data_type=data_type,
            defaults={'bearer_token': 'foobars'}
        )

        if data_set_created:
            print "Created data set" + data_group_name + " " + data_type_name + " " + new_data_type_name
        else:
            print "Data set already existed" + data_group_name + " " + data_type_name + " " + new_data_type_name

        excluded_query_parameters = ['duration']

        query_parameters = {
            param: value for param, value in module.query_parameters.iteritems() if param not in excluded_query_parameters
        }

        transform = {
            "type_id": transform_type_id,
            "input": {
                "data-group": data_group_name,
                "data-type": data_type_name,
            },
            "query-parameters": query_parameters,
            "options": {transform_option: module.options[spotlight_option] for transform_option, spotlight_option in metadata['options'].iteritems()},
            "output": {
                "data-group": data_group_name,
                "data-type": new_data_type_name,
            }
        }

        r = requests.post(
            STAGECRAFT_ROOT + '/transform', data=json.dumps(transform), headers=headers)

        if r.status_code != 200:
            print r.text
            exit('Received error from Stagecraft when making Transform: ' + data_group_name + ' ' + new_data_type_name)

print "Finished creating TransformTypes and Transforms."
