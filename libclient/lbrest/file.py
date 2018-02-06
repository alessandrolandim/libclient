# -*- coding: utf-8 -*-
import os
import uuid

from .core import LBRest
from ..lbtypes.base import Base
from ..lbtypes.file import File

from ..lbsearch.search import Search
from ..lbsearch.search import FileCollection

from ..utils import json2object

class FileREST(LBRest):

    """
    Contains methods for handling LightBase files via via Lightbase's REST API.
    """

    def __init__(self, rest_url, base, response_object=False):
        """
        Class constructor.

        @param rest_url: the REST URL.
        @param base (string or Base): the base's name or a Base object (libclient.lbtypes.base.Base)
        """
        super(FileREST, self).__init__(rest_url, response_object)
        if isinstance(base, Base) or isinstance(base, PYSTR):
            self.base = base
        else:
            raise TypeError("Wrong parameter: not a base or string, but {}".format(type(base)))


    def create(self, file):
        """
        Creates file.

        @param file (tuple): containg filename (string) and file contents (bytes).
            Ex: ('name.txt', b'\123\334_file_contents_\334\123')
        """
        if isinstance(file, File):
            file_param = (file.filename, file.content)
        elif isinstance(file, tuple):
            file_param = file
        else:
            raise TypeError('Wrong parameter: files must be a 2-valued tuple containg: file name and file content')

        response = self.send_request(self.httppost,
            url_path=[self.basename, self.file_prefix],
            files={self.file_param : file_param})
        return json2object(response)


    def get(self, id):
        """
        Retrieves file by id, returns file's headers and binary. 

        @param id (int): the file identify.
        """
        response = self.send_request(self.httpget,
            url_path=[self.basename, self.file_prefix, str(id)])
        response_dict = json2object(response)
        file = File.from_dict(response_dict)
        return file

    def get_content(self, id):
        """
        Retrieves file by id, returns file's headers and binary. 

        @param id (int): the file identify.
        """
        response = self.send_request(self.httpget,
            url_path=[self.basename, self.file_prefix, str(id), 'download'],
            stream=True, response_object=True)
        return response.content

    def get_collection(self, search_obj=None):
        """
        Retrieves collection of "file text" according to search object.

        @param search_obj (Search, optional, default=None): a Search object (libclient.lbsearch.search.Search) 
            with the search attributes.
        """
        if search_obj is not None:
            msg = 'search_obj must be a Search object.'
            assert isinstance(search_obj, Search), msg
        else:
            search_obj = Search()
        response = self.send_request(self.httpget,
            url_path=[self.basename, self.file_prefix],
            params={self.search_param: search_obj.as_json()})
        return FileCollection(**json2object(response))

    def get_path(self, id, path):
        """
        Retrieves a file attribute by id.

        @param id: the file identify.
        @param path: the file attribute to be retrieved. Possible values are:
            -filetext;
            -filesize;
            -filename;
            -mimetype;
            -id_doc;
            -id_file;
            -dt_ext_text
        """
        return self.send_request(self.httpget,
            url_path=[self.basename, self.file_prefix, str(id), path])

    def _get_file_headers(self, response):
        cd = response.headers['Content-Disposition']
        return {
            'filename': cd[cd.rfind("=") + 1:].strip(),
            'mimetype': response.headers['Content-Type']
        }

    def download(self, id):
        """ Alias to @method get 
        """
        return self.get(id)


    def upload(self, files):
        """ 
        Alias to @method create
        """
        return self.create(files)

    # TODO
    def update(self):
        """
        """
        pass

    # TODO
    def delete(self):
        """
        """
        pass
