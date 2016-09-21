import os
import simplejson as json

__all__ = ['get_raw_resource', 'get_raw_json_resource', 'get_json_resource']


def get_raw_resource(name, extension):
    filename = '%s.%s' % (name, extension)
    file_path = os.path.join('tests', 'resources', filename)
    with open(file_path, 'r') as f:
        return f.read()


def get_raw_json_resource(name):
    return get_raw_resource(name, 'json')


def get_json_resource(name):
    """
    Will parse the JSON of a given test resource. For a name of 'spurs', this will parse the
    file 'test/resources/spurs.json
    :param name: name of the resource
    :return: dict
    """
    return json.loads(get_raw_json_resource(name), use_decimal=True)
