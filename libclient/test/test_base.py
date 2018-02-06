import unittest
from requests.exceptions import HTTPError

from ..lbrest.base import BaseREST
from ..lbtypes.base import *
from ..utils import json2object

class TestBaseREST(unittest.TestCase):

    def setUp(self):
        self.rest = BaseREST('http://192.168.56.102')
        self.basename = 'python_rest_test'

    def test_1_create(self):
        base = Base(name=self.basename)
        group = Group(name='group')
        field1 = Field(name='field1', datatype='Text', required=True)
        group.add_field(field1)
        field2 = Field(name='field2', datatype='Text')
        group.add_field(field2)
        base.add_field(group)

        response = self.rest.create(base)
        self.assertIsNotNone(response)
        base_id = int(response)
        self.assertIsInstance(base_id, int)
        self.assertGreater(base_id, 0)

    # TODO: search error

    def test_2_get(self):
        response = self.rest.get(self.basename)
        self.assertIsNotNone(response)
        self.assertIsInstance(response, Base)
        self.assertEqual(response.metadata.name, self.basename)
    

    def test_2_get_as_dict(self):
        response = self.rest.get(self.basename, as_dict=True)
        self.assertIsNotNone(response)
        self.assertIsInstance(response, dict)
        self.assertEqual(response['metadata']['name'], self.basename)


    def test_2_get_error(self):
        self.assertRaises(HTTPError, self.rest.get, *['not_a_base'])


    def test_2_get_path(self):
        response = self.rest.get_path(self.basename, 'group/field1')
        self.assertIsNotNone(response)
        self.assertEqual(response, 
            json2object(Field('field1', 'Text', required=True).get_json()))

    def test_2_search(self):
        response = self.rest.search()
        self.assertIsNotNone(response)
        self.assertIsNotNone(response['result_count'])

    # TODO: search with select
    # TODO: search with literal
    # TODO: search with (etc...)


    # TODO:!!!!    
    # def test_3_update(self):
    #     base = Base('python_rest_test')
    #     group = Group('group_changed')
    #     field1 = Field('field1_changed', 'Text', required=True)
    #     group.add_field(field1)
    #     field2 = Field('field2_changed', 'Text')
    #     group.add_field(field2)
    #     base.add_field(group)

    #     response = self.rest.update(base)
    #     self.assertIsNotNone(response)
    #     self.assertEqual(response, 'UPDATED')

    def test_4_delete(self):
        response = self.rest.delete(self.basename)
        self.assertIsNotNone(response)
        self.assertEqual(response, 'DELETED')


if __name__ == '__main__':
    unittest.main()