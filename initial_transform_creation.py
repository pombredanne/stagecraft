from django.conf import settings

from stagecraft.apps.datasets.models.data_group import DataGroup
from stagecraft.apps.datasets.models.data_type import DataType

import json
import requests

if 'development' in settings.APP_HOSTNAME:
    HTTP_PROTOCOL = 'http'
else:
    HTTP_PROTOCOL = 'https'

STAGECRAFT_ROOT = '{0}://{1}'.format(HTTP_PROTOCOL, settings.APP_HOSTNAME)

transform_type = {
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

headers = {
    'Authorization': 'Bearer {0}'.format(settings.MIGRATION_SIGNON_TOKEN),
    'Content-Type': 'application/json',
}

r = requests.post(STAGECRAFT_ROOT + '/transform-type',
                  data=json.dumps(transform_type), headers=headers)

print r.status_code,
print r.content

transform_type_id = r.json()['id']


def find_modules(dashboards):
    for dashboard in dashboards:
        modules = requests.get(STAGECRAFT_ROOT + '/public/dashboards?slug=' + dashboard['slug'], headers=headers).json()['modules']
        for module in modules:
            if module['module-type'] == 'completion_rate':
                yield module


dashboards = requests.get(STAGECRAFT_ROOT + '/public/dashboards', headers=headers).json()['items']

for module in find_modules(dashboards):
    data_group_name = module['data-source']['data-group']
    data_type_name = module['data-source']['data-type']
    new_data_type_name = module['data-source']['data-type'] + '-rate'

    (data_group, data_group_created) = DataGroup.objects.get_or_create(name=data_group_name)
    (data_type, data_type_created) = DataType.objects.get_or_create(name=new_data_type_name)

    if data_group_created:
        exit('Data group did not exist before script started')

    transform = {
        "type_id": transform_type_id,
        "input": {
            "data-group": data_group_name,
            "data-type": data_type_name,
        },
        "query-parameters": module['data-source']['query-params'],
        "options": {
            "denominatorMatcher": module['denominator-matcher'],
            "numeratorMatcher": module['numerator-matcher'],
            "matchingAttribute": module['matching-attribute'],
            "valueAttribute": module['value-attribute'],
        },
        "output": {
            "data-group": data_group_name,
            "data-type": new_data_type_name,
        }
    }

    r = requests.post(
        STAGECRAFT_ROOT + '/transform', data=json.dumps(transform), headers=headers)

    print r.status_code
