from django.contrib.auth.models import User
import requests
from rest_framework.test import APITestCase
from faker import Faker
from abc import ABC
import re
from drf_util.utils import gt


# Create your tests here.
class AbstractClass(ABC):
    def __init__(self, api):
        self.response = api
        self.data = self.response.json()
        self.paths = self.data.get('paths', {})
        self.definitions = self.data.get('definitions', {})
        self.fake = Faker(['nl_NL'])

    urls = []
    endpoint_work_time = '/work-time/'

    def execution_method(self, path, http_method):
        id_path = re.findall('\d', path)
        for endpoint, methods in self.paths.items():
            for method in methods.items():
                http_method_name, options = method
                if http_method_name == 'parameters':
                    continue
                try:
                    endpoint = endpoint.format(**{"id": id_path[0]})
                except IndexError:
                    pass
                if http_method_name == http_method and endpoint == path:

                    params = options.get('parameters', [])
                    body_payload = next(
                        iter([body_object for body_object in params if body_object.get('in', '') == 'body']))
                    definition = gt(body_payload, 'schema.$ref', None)
                    if not definition or not isinstance(definition, str):
                        continue
                    elements = definition.split('/')
                    element = elements[len(elements) - 1]
                    model = gt(self.definitions, f'{element}.properties', {})
                    keys = [key for key in model.keys() if key != 'id']
                    payload = {}
                    for key in keys:
                        if gt(self.definitions, f'{element}.properties.{key}.format', {}) != 'date-time':
                            payload.update({key: self.fake.name()})
                        else:
                            payload.update({key: self.fake.date_time_this_month(after_now=True)})
                    return payload

    def execution_post_method(self, path: str, client) -> dict:
        data = client.post(f'http://localhost:8000{path}', data=self.execution_method(path, http_method='post'))
        return data.json()

    def execution_get_method(self, path, client):
        id_path = re.findall('\d', path)
        for endpoint, methods in self.paths.items():
            for method in methods.items():
                http_method_name, options = method
                if http_method_name == 'parameters':
                    continue
                try:
                    endpoint = endpoint.format(**{"id": id_path[0]})
                except IndexError:
                    pass
                if http_method_name == 'get' and endpoint == path:
                    data = client.get(f'http://localhost:8000{path}')
                    return data.json()

    def execution_put_method(self, path, client):
        data = client.put(f'http://localhost:8000{path}', data=self.execution_method(path, http_method='put'))
        return data.json()

    def execution_delete_method(self, path, client):
        data = client.delete(f'http://localhost:8000{path}')
        return data


class ManagerTest(APITestCase, AbstractClass):
    def setUp(self) -> None:
        user_test1 = User.objects.create(username='admin', password='admin')
        self.object = AbstractClass(requests.get('http://127.0.0.1:8000/?format=openapi'))
        self.client.force_authenticate(user=user_test1)
