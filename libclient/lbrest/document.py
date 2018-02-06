# -*- coding: utf-8 -*-
from six import string_types as PYSTR

from .core import LBRest
from ..lbtypes.base import Base

from ..utils import json2object
from ..utils import object2json

from ..lbsearch.search import Search
from ..lbsearch.search import Collection


class DocumentREST(LBRest):
    """ 
    Contains methods for handling Lightbase Documents via Lightbase's REST API.
    """

    def __init__(self, rest_url, base, response_object=False):
        """
        Class constructor.

        @param rest_url (string): Lighbase's REST API URL.
        @param base (string or Base): the base's name or a Base object (libclient.lbtypes.base.Base)
        @param response_object (boolean, optional, default=False: if true, 
            calls to methods will return python's response objects (for debugging).
        """
        super(DocumentREST, self).__init__(rest_url, response_object)
        if isinstance(base, Base) or isinstance(base, PYSTR):
            self.base = base
        else:
            raise TypeError("Wrong parameter: not a base or string, but {}".format(type(base)))

    def create(self, document):
        """
        Creates new document.

        @param document (dict): the document being created.
        """
        if not isinstance(document, dict):
            raise TypeError('Wrong parameter: document must be a dictionary')

        response = self.send_request(self.httppost,
                                     url_path=[self.basename,
                                               self.doc_prefix],
                                     data={self.doc_param: object2json(document)})
        return int(response)

    def get(self, id):
        """
        Retrieves document by id.

        @param id (int): the document's id.
        """
        if not isinstance(id, int):
            raise TypeError('Wrong parameter: id must be an int')
        
        response = self.send_request(self.httpget,
                                     url_path=[self.basename, self.doc_prefix, str(id)])

        return json2object(response)

    def get_path(self, id, path):
        """
        Retrieves given path on document.

        @param id (int): The document identify.
        @param path (string or list): path on document to be retrieved,
            if string segments must be separated by '/',
            if list each element is a string containing a segment of the path.
        """
        if not isinstance(id, int):
            raise TypeError('Wrong parameter: id must be an int')

        path_list = [self.basename, self.doc_prefix, str(id)]
        if isinstance(path, PYSTR):
            for p in path.split('/'):
                path_list.append(p)
        elif isinstance(path, list):
            path_list += path
        else:
            raise TypeError('Wrong parameter: path must be a list or string')

        response = self.send_request(self.httpget, url_path=path_list)
        return json2object(response)

    def search(self, search_obj=None):
        """
        Retrieves collection of documents according to search object or
            all documents if search_obj=None.

        @param search_obj (Search): a Search object (libclient.lbsearch.search.Search) 
            with the search attributes.
        """
        search_obj = search_obj or Search()
        
        if not isinstance(search_obj, Search):
            raise TypeError('search_obj must be a Search object.')

        response = self.send_request(self.httpget,
                                     url_path=[self.basename, self.doc_prefix],
                                     params={self.search_param: search_obj.as_json()})

        return json2object(response)

    def update(self, id, document):
        """
        Updates document by id.

        @param id (int): the document identify.
        @param document (dict): updated Document.
        """
        return self.send_request(self.httpput,
                                 url_path=[self.basename, self.doc_prefix, str(id)],
                                 data={self.doc_param: object2json(document)})

    def create_path(self, id, path, value):
        """
        Creates given path on document.

        @param id (int): the document identify.
        @param path (string or list): path on document to the field that will be created,
            if string segments must be separated by '/',
            if list each element is a string containing a segment
        @param value: the value to create on path.
        """
        if not isinstance(id, int):
            raise TypeError('Wrong parameter: id must be an int')

        path_list = [self.basename, self.doc_prefix, str(id)]
        if isinstance(path, PYSTR):
            for p in path.split('/'):
                path_list.append(p)
        elif isinstance(path, list):
            path_list += path
        else:
            raise TypeError('Wrong parameter: path must be a list or string')

        if isinstance(value, list) or isinstance(value, dict):
            value = object2json(value)

        return self.send_request(self.httppost,
                                 url_path=path_list,
                                 data={self.doc_param: value})

    def update_path(self, id, path, value):
        """
        Updates given path on document.
        @param id (int): the document identify.
        @param path (string or list): path on document to be updated,
            if string segments must be separated by '/',
            if list each element is a string containing a segment
        @param value (any): the value to update on path.
        """
        if not isinstance(id, int):
            raise TypeError('Wrong parameter: id must be an int')

        path_list = [self.basename, self.doc_prefix, str(id)]
        if isinstance(path, PYSTR):
            for p in path.split('/'):
                path_list.append(p)
        elif isinstance(path, list):
            path_list += path
        else:
            raise TypeError('Wrong parameter: path must be a list or string')

        return self.send_request(self.httpput,
                                 url_path=path_list,
                                 data={self.doc_param: object2json(value)})

    def update_collection(self, path, value=None, search_obj=None):
        """
        Updates collection of documents according to search object.

        @param path (string or list of dicts): path on documents to be updated,
            if string segments must be separated by '/',
            if list each element is a dict with of following keys:
                - path (string): path of field that will be updated
                - mode (string): 'update'
                - args (list): list of new values that will replace the current values
                (for more information see: http://mediawiki.brlight.net/index.php/Rotas_do_REST#Alterar_n.C3.B3_de_Documentos)
        @param value (list, optional, default=None): list of new values that 
            will replace the current values. This is only needed if 'path' is a string
        @param search_obj (Search, optional, default=None): a Search object 
            (libclient.lbsearch.search.Search) that will determine which documents
            will be updated
        """
        if search_obj is not None and not isinstance(search_obj, Search):
            raise TypeError('search_obj must be a Search object.')
        else:
            search_obj = Search()

        path_param = []
        if isinstance(path, PYSTR):
            path_dict = {
                'path': path,
                'mode': 'update',
                'args': value
            }
            path_param.append(path_dict)
        elif isinstance(path, list):
            if len(path) > 0 and not isinstace(path[0], dict):
                raise TypeError('Wrong parameter: path list must contain dictionaries')

            path_param = path
        else:
            raise TypeError('Wrong parameter: path must be a list or string')

        response = self.send_request(self.httpput,
                                     url_path=(self.basename, self.doc_prefix),
                                     params={self.search_param: search_obj.as_json(),
                                             self.path_param: object2json(path_param)})

        return json2object(response)

    def delete(self, id):
        """
        Deletes document by id.

        @param id (int): the document identify.
        """
        return self.send_request(self.httpdelete,
                                 url_path=[self.basename,
                                           self.doc_prefix,
                                           str(id)])

    def delete_path(self, id, path):
        """
        Deletes fields given by the path on document.

        @param id(int): the document identify.
        @param path (string or list): path of the fields that will be deleted,
            if string segments must be separated by '/',
            if list each element is a string containing a segment
        """

        if not isinstance(id, int):
            raise TypeError('Wrong parameter: id must be an int')

        path_list = [self.basename, self.doc_prefix, str(id)]
        if isinstance(path, PYSTR):
            for p in path.split('/'):
                path_list.append(p)
        elif isinstance(path, list):
            path_list += path
        else:
            raise TypeError('Wrong parameter: path must be a list or string')

        return self.send_request(self.httpdelete, url_path=path_list)

    def delete_collection(self, path=None, search_obj=None):
        if path is not None and not isinstance(path, (PYSTR, list)):
            raise TypeError('Wrong parameter: ' +
                            'path (optional) must be str or list of dict')

        search_obj = search_obj or Search()

        if not isinstance(search_obj, Search):
            raise TypeError('Wrong parameter: search_obj must be a Search')

        path_param = object2json(path) if path is not None else None
        method = self.httpdelete\
            if path is None or isinstance(path, PYSTR) \
            else self.httpput

        response = self.send_request(method,
                                     url_path=(self.basename, self.doc_prefix),
                                     params={self.search_param: search_obj.as_json(),
                                             self.path_param: path_param})

        return json2object(response)
