import json

import requests

from tests.utils.login import login, url


def test_crud_units():
    headers = login()

    requests.post(url('units'), headers=headers, data=json.dumps({
        'shortname': 'test_unit',
        'name': 'test_name'
    }))

    units = requests.get(url('units'), headers=headers)
    assert units.json() ==  {'items': [{'name': 'Kilocalorías', 'shortname': 'Kcal'}, {'name': 'gram', 'shortname': 'g'}, {'name': 'kilogram', 'shortname': 'kg'}, {'name': 'test_name', 'shortname': 'test_unit'}]}

    requests.put(url('units/test_unit'), headers=headers, data=json.dumps({
        'shortname': 'test_unit',
        'name': 'test_name2'
    }))

    units = requests.get(url('units'), headers=headers)
    assert units.json() ==  {'items': [{'name': 'Kilocalorías', 'shortname': 'Kcal'}, {'name': 'gram', 'shortname': 'g'}, {'name': 'kilogram', 'shortname': 'kg'}, {'name': 'test_name2', 'shortname': 'test_unit'}]}

    requests.delete(url('units'), headers=headers, data=json.dumps({
        'shortname': 'test_unit',
        'name': 'test_name'
    }))
    units = requests.get(url('units'), headers=headers)
    assert units.json() ==  {'items': [{'name': 'Kilocalorías', 'shortname': 'Kcal'}, {'name': 'gram', 'shortname': 'g'}, {'name': 'kilogram', 'shortname': 'kg'}]}