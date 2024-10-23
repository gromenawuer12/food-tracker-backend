import json

import requests

from tests.utils.login import login, url


def test_crud_settings():
    headers = login()

    requests.post(url('settings'), headers=headers, data=json.dumps({
        'shortname': 'test_unit',
        'partsOfDay': 'test_name'
    }))

    units = requests.get(url('settings/test_unit'), headers=headers)
    assert units.json() ==  {'partsOfDay': 'test_name', 'shortname': 'test_unit'}

    requests.post(url('settings'), headers=headers, data=json.dumps({
        'shortname': 'test_unit',
        'partsOfDay': 'test_name2'
    }))

    units = requests.get(url('settings/test_unit'), headers=headers)
    assert units.json() ==  {'partsOfDay': 'test_name2', 'shortname': 'test_unit'}