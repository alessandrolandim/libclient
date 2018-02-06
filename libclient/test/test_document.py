import re
import unittest

from ..lbrest.base import BaseREST
from ..lbrest.document import DocumentREST
from ..lbtypes.base import *
from ..lbsearch.search import Search


class TestDocumentREST(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # prepare base for tests
        cls.basename = 'python_rest_test'
        cls.base_rest = BaseREST('http://192.168.56.102')
        cls.base = cls._create_base()

        cls.rest = DocumentREST('http://192.168.56.102', cls.base)
        cls.test_doc = {
            'txt_title': 'Sehnsucht',
            'gp_artists': [
                {
                    'bool_is_band': False,
                    'txt_artist_name': 'Rammstein'
                }
            ],
            'gp_tracks': [
                {
                    "txt_track_title": "Sehnsucht",
                    "int_track_number": 1,
                    "time_track_len": "04:04:00"
                }, {
                    "txt_track_title": "Tier",
                    "int_track_number": 3,
                    "time_track_len": "03:48:00"
                }, {
                    "txt_track_title": "Du Hast",
                    "int_track_number": 5,
                    "time_track_len": "03:54:00"
                },
            ]
        }

    @classmethod
    def tearDownClass(cls):
        # delete test base
        cls._delete_base()

    def test_1_create(self, expected_id=1):
        doc_id = self.rest.create(self.test_doc)
        self.assertIsNotNone(doc_id)
        self.assertIsInstance(doc_id, int)
        self.assertEqual(doc_id, expected_id)

    def test_2_get(self):
        doc = self.rest.get(1)
        self.assertIsNotNone(doc)
        for key in list(doc.keys()):
            if key.startswith('_'):
                doc.pop(key)
        self.assertEqual(doc, self.test_doc)

    def test_2_get_path(self):
        path = self.rest.get_path(1, 'gp_tracks/2/txt_track_title')
        self.assertIsNotNone(path)
        self.assertEqual(
            path, self.test_doc['gp_tracks'][2]['txt_track_title'])

    def test_2_search(self):
        # TODO: test search options
        response = self.rest.search()
        self.assertIsNotNone(response)
        first = response['results'][0]
        for key in list(first.keys()):
            if key.startswith('_'):
                    first.pop(key)
        self.assertEqual(first, self.test_doc)

    def test_3_update(self):
        doc = self.test_doc.copy()
        doc['gp_artists'][0]['txt_artist_name'] = 'Rammstein (updated)'
        response = self.rest.update(1, doc)
        self.assertIsNotNone(response)
        self.assertEqual(response, 'UPDATED')
        updated_doc = self.rest.get(1)
        for key in list(updated_doc.keys()):
            if key.startswith('_'):
                    updated_doc.pop(key)
        self.assertEqual(updated_doc, doc)

    def test_3_create_path(self):
        path = 'gp_tracks'
        value = {
            "txt_track_title": "Spiel Mit Mir",
            "int_track_number": 7,
            "time_track_len": "04:44:00"
        }
        full_list = self.test_doc['gp_tracks']
        full_list.append(value)
        response = self.rest.create_path(1, path, value)
        self.assertEqual(response, 'OK')
        updated_list = self.rest.get_path(1, path)
        self.assertEqual(updated_list, full_list)

    def test_3_update_path(self):
        path = 'gp_tracks/0/txt_track_title'
        value = 'Sehnsucht (updated)'
        response = self.rest.update_path(1, path, value)
        self.assertEqual(response, 'UPDATED')
        updated_value = self.rest.get_path(1, path)
        updated_value = re.sub(r"^\"", '', updated_value)
        updated_value = re.sub(r"\"$", '', updated_value)
        self.assertEqual(updated_value, value)

    def test_3_update_collection(self):
        path = 'gp_tracks/*/txt_track_title'
        value = ['No Track Title']
        search = Search(literal='txt_title = \"Sehnsucht\"')
        response = self.rest.update_collection(path, value=value, search_obj=search)
        self.assertIsInstance(response, dict)
        self.assertEqual(response['success'], 1)
        self.assertEqual(response['failure'], 0)
        updated_path = self.rest.get_path(1, 'gp_tracks/*/txt_track_title')
        self.assertIsNotNone(updated_path)
        self.assertIsInstance(updated_path, dict)
        for k, v in updated_path.items():
            self.assertEqual(v, 'No Track Title')

    # TODO: update_collection test: 
        # path = dict
        # single path and single value
        # path = list of strings?

    def test_4_delete_path(self):
        path = 'gp_tracks'
        response = self.rest.delete_path(1, path=path)
        self.assertEqual(response, 'DELETED')
        updated_doc = self.rest.get(1)
        self.assertIsNone(getattr(updated_doc, 'gp_tracks', None))

    def test_5_delete(self):
        response = self.rest.delete(1)
        self.assertEqual(response, 'DELETED')

    # TODO: delete_collection test
    def test_6_delete_collection(self):
        for i in range(2, 5):
            self.test_1_create(expected_id=i)

        search_params = Search(literal="txt_title = 'Sehnsucht'")
        response = self.rest.delete_collection(search_obj=search_params)
        self.assertIsNotNone(response)
        collection = self.rest.search()
        self.assertEqual(len(collection['results']), 0)

    def test_7_delete_collection_path(self):
        for i in range(5, 8):
            self.test_1_create(expected_id=i)

        path_list = [{
            'path': 'gp_tracks/*',
            'mode': 'delete',
            'fn': 'attr_equals',
            'args': ['txt_track_title', 'Tier']
        }]
        response2 = self.rest.delete_collection(path=path_list)
        self.assertIsNotNone(response2)
        self.assertEqual(response2['failure'], 0,
                         msg='Failed to delete collection. Result = {}'
                         .format(str(response2)))
        collection2 = self.rest.search()
        for album in collection2['results']:
            for track in album['gp_tracks']:
                self.assertNotEqual(track['txt_track_title'], 'Tier')

    @classmethod
    def _create_base(cls):
        # model = {
        #     "img_cover": "Image",
        #     "txt_title": "Text",
        #     "gp_artists": [
        #         {
        #           "bool_is_band": "Boolean",
        #           "txt_artist_name": "Text"
        #         }
        #     ],
        #     "gp_tracks": [
        #         {
        #             "txt_track_title": "Text",
        #             "int_track_number": "Integer",
        #             "snd_file": "Sound",
        #             "time_track_len": "Time"
        #         }
        #     ]
        # }

        base = Base(metadata=BaseMetadata(cls.basename))

        # field txt_title
        base.add_field(Field(name='txt_title', datatype='Text', required=True))

        # field img_cover
        base.add_field(Field(name='img_cover', datatype='Image', required=False,
            alias='Title', description='Album Title'))

        # group gp_artists
        gp_artists = Group(name='gp_artists', multivalued=True)
        gp_artists.add_field(Field(name='bool_is_band', datatype='Boolean', 
            required=True))
        gp_artists.add_field(Field(name='txt_artist_name', datatype='Text',
            required=True))
        base.add_field(gp_artists)

        # group gp_tracks
        gp_tracks = Group(name='gp_tracks', multivalued=True)
        gp_tracks.add_field(Field(name='txt_track_title', datatype='Text', required=True))
        gp_tracks.add_field(Field(name='int_track_number', datatype='Integer', required=False))
        gp_tracks.add_field(Field(name='snd_file', datatype='Sound', required=False))
        gp_tracks.add_field(Field(name='time_track_len', datatype='Time', required=False))
        base.add_field(gp_tracks)

        response = cls.base_rest.create(base)
        base_id = int(response)
        base = cls.base_rest.get(cls.basename)
        return base


    @classmethod
    def _delete_base(cls):
        cls.base_rest.delete(cls.basename)


if __name__ == '__main__':
    unittest.main()