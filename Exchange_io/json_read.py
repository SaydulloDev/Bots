import json


def json_api_reader(res):
    data = res
    parsed_data = json.loads(data)
    rates = parsed_data['rates']
    return rates
