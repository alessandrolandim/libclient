import unittest

from ..lbrest.base import BaseREST
from ..lbrest.document import DocumentREST
from ..lbrest.file import FileREST
from ..lbtypes.base import *
from ..lbtypes.file import File
from ..lbsearch.search import Search

class TestFileREST(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # prepare base for tests
        cls.basename = 'python_rest_test'
        cls.base_rest = BaseREST('http://192.168.56.102')
        cls.base = cls._create_base()

        # prepare document for tests
        cls.doc_rest = DocumentREST('http://192.168.56.102', cls.base)
        cls._create_doc()

        cls.rest = FileREST('http://192.168.56.102', cls.base)
        cls.filepath = 'libclient/test/files/'


    @classmethod
    def tearDownClass(cls):
        # delete test base
        cls._delete_base()


    def test_1_create_txt(self):
        filename = 'file_for_testing.txt'
        file = File.open(self.filepath + filename)
        response = self.rest.create(file)
        self.assertIsInstance(response, dict)
        self.assertEqual(response['filename'], filename)
        self.assertIsNotNone(response.get('uuid', None))
        self.assertIsNotNone(response.get('id_file', None))
        cls = type(self)
        cls.file_txt = response
        cls.file_txt_contents = file.content


    def test_1_create_image(self):
        filename = 'sehnsucht.png'
        file = open(self.filepath + filename, 'rb')
        file_contents = file.read()
        file.close()
        response = self.rest.create((filename, file_contents))
        self.assertIsInstance(response, dict)
        self.assertEqual(response['filename'], filename)
        self.assertIsNotNone(response.get('uuid', None))
        self.assertIsNotNone(response.get('id_file', None))
        cls = type(self)
        cls.file_img = response
        cls.file_img_contents = file_contents


    def test_2_associate_with_doc(self):
        response = self.doc_rest.update_path(1, 'img_cover', self.file_img)
        self.assertEqual(response, 'UPDATED')
        updated_doc = self.doc_rest.get(1)
        self.assertIsNotNone(updated_doc)
        self.assertIsNotNone(updated_doc.get('img_cover', None))
        self.assertEqual(updated_doc['img_cover'], self.file_img)


    def test_3_get(self):
        file = self.rest.get(self.file_txt['id_file'])
        self.assertEqual(file.filename, self.file_txt['filename'])
        self.assertEqual(file.filesize, self.file_txt['filesize'])
        self.assertEqual(file.id_file, self.file_txt['id_file'])


    def test_3_get_content_txt(self):
        content = self.rest.get_content(self.file_txt['id_file'])
        self.assertTrue(content == self.file_txt_contents,
            msg='Different file contents (image)')
        file = open(self.filepath + 'retrieved_txt_file.txt', 'wb')
        file.write(content)
        file.close()

    def test_3_get_content_img(self):
        content = self.rest.get_content(self.file_img['id_file'])
        self.assertTrue(content == self.file_img_contents,
            msg='Different file contents (image)')
        file = open(self.filepath + 'retrieved_img_file.png', 'wb')
        file.write(content)
        file.close()


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

        base = Base(name=cls.basename)

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
    def _create_doc(cls):
        cls.doc = {
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
                },{
                    "txt_track_title": "Tier",
                    "int_track_number": 3,
                    "time_track_len": "03:48:00"
                },{
                    "txt_track_title": "Du Hast",
                    "int_track_number": 5,
                    "time_track_len": "03:54:00"
                },
            ] 
        }
        cls.doc_id = cls.doc_rest.create(cls.doc)


    @classmethod
    def _delete_base(cls):
        cls.base_rest.delete(cls.basename)


if __name__ == '__main__':
    unittest.main()