# -*- coding: utf-8 -*-
from six import string_types as PYSTR

from .core import LBRest
from ..utils import json2object
from ..utils import object2json
from ..lbtypes.base import Base
from ..lbsearch.search import Search


class BaseREST(LBRest):
    """
    Contains methods for handling Lightbase Bases via Lightbase's REST API.
    """

    def __init__(self, rest_url, response_object=False):
        """
        @param rest_url (string): url address of LBGenerator's REST
        """
        super(BaseREST, self).__init__(rest_url, response_object)

    def create(self, base):
        """
        @param base (string or lbtypes.Base): a string with the base's name or
            a lbtype.Base instance
        """
        if isinstance(base, dict):
            base_json = object2json(base)
        elif isinstance(base, Base):
            base_json = base.get_json()
        else:
            raise TypeError('Wrong parameter: base must be a lbtypes.Base or a dict')

        response = self.send_request(self.httppost, data={self.base_param: base_json})

        return int(response)

    def get(self, basename, as_dict=False):
        """
        Retrieves the base with name 'basename'

        @param basename (string): the base's name
        @param as_dict (boolean, optional, default=False): if False,
            returns an lbtype.Base instance; if True, returns a dict
            with base's metadata
        """
        if not isinstance(basename, PYSTR):
            raise TypeError('basename must be a string.')

        response = self.send_request(self.httpget,
                                     url_path=[basename])

        dict_base = json2object(response)

        if as_dict:
            return dict_base

        return Base.from_dict(dict_base)

    def get_by_id(self, id_base, as_dict=False):
        """
        Retrieves the base with id 'id_base'

        @param basename (int): the base's id
        @param as_dict (boolean, optional, default=False): if False,
            returns an lbtype.Base instance; if True, returns a dict
            with base's metadata
        """
        if not isinstance(id_base, int):
            raise TypeError('id_base must be an int')

        literal = 'id_base = %d' % id_base
        search_obj = Search(literal=literal)
        response = self.send_request(
            self.httpget, params={self.search_param: search_obj.as_json()})

        dict_base = json2object(response)

        if as_dict:
            return dict_base

        return Base.from_dict(dict_base)

    def get_path(self, basename, path=''):
        """
        Retrieves metadata for the fields pointed by 'path'.

        @param basename (string): the base's name
        @param path (string, optiona, default=''): path of attributes
            to be retrieved with path segments separated by slash '/'
            Ex: 'path/to/document/attributes'
        """
        path_list = [basename]
        for p in path.split('/'):
            path_list.append(p)

        response = self.send_request(self.httpget, url_path=path_list)

        return json2object(response)

    # TODO: return as_dict parameter
    def search(self, search_obj=None):
        """
        Retrieves a collection of bases that match search_obj's 
        attributes or all bases if search_obj is None.

        @param search_obj (lbsearch.Search, optional, default=None'):
        """
        search_obj = search_obj or Search()

        if search_obj is not None and not isinstance(search_obj, Search):
            raise TypeError('search_obj must be a Search object.')

        response = self.send_request(self.httpget,
            params={self.search_param: search_obj.as_json()})

        return json2object(response)

    # TODO TODO TODO!!!
    def update(self, base):
        """
        Updates base's metadata.

        @param base (string or lbtypes.Base): a string with the base's name or
            a lbtype.Base instance
        """
        if isinstance(base, dict):
            base_json = object2json(base)
        elif isinstance(base, Base):
            base_json = base.get_json()
        else:
            raise TypeError('Wrong parameter: base must be a lbtypes.Base or a dict')

        return self.send_request(self.httpput, url_path=[base.metadata.name],
                                 data={self.base_param: base_json})

    def delete(self, base):
        """
        Deletes base.

        @param base (string): the base's name
        """
        if isinstance(base, Base):
            basename = base.metadata.name
        elif isinstance(base, PYSTR):
            basename = base
        else:
            raise TypeError('basename must be a string.')
        
        return self.send_request(self.httpdelete,
                                 url_path=[basename])

    def create_txt_idx(self, base):
        """
        @param base:
        """
        print(str(base["metadata"]["idx_exp_url"]))
        if(base["metadata"]["idx_exp_url"] is not ''):
            print('159')
            str_idx_exp_url = str(base["metadata"]["idx_exp_url"])
            print(str_idx_exp_url)
            arr_idx_exp_url = str_idx_exp_url.split('/')
            print(str(len(arr_idx_exp_url)))
            if len(arr_idx_exp_url) == 5:
                str_idx_exp_url = arr_idx_exp_url[0] + '//' + arr_idx_exp_url[2] + '/' + arr_idx_exp_url[3]
                print(str_idx_exp_url)
                txt_idx = {
                    "nm_idx":str(base["metadata"]["name"]),
                    "cfg_idx":{
                        "analysis":{
                            "char_filter":{
                                "alfanumeric_pattern":{
                                    "type":"pattern_replace",
                                    "pattern":"[^a-zA-Z0-9]",
                                    "replacement":""
                                },
                                "mapping_filter":{
                                    "type":"mapping",
                                    "mappings":[
                                        "-\\n=>"
                                    ]
                                }
                            },
                            "tokenizer":{
                                "ngram_tokenizer":{
                                    "min_gram":"2",
                                    "type":"ngram",
                                    "max_gram":"3",
                                    "token_chars":[
                                        "digit",
                                        "letter"
                                    ]
                                }
                            },
                            "filter":{
                                "stemmer_pt_br":{
                                    "type":"stemmer",
                                    "name":"brazilian"
                                },
                                "numeric_filter":{
                                    "type":"pattern_replace",
                                    "pattern":"[^0-9]",
                                    "replacement":""
                                },
                                "leading_zeroes_filter":{
                                    "type":"pattern_replace",
                                    "pattern":"^0+",
                                    "replacement":""
                                }
                            },
                            "analyzer":{
                                "keyword_analyzer":{
                                    "tokenizer":"keyword"
                                },
                                "ngram_analyzer":{
                                    "char_filter":[
                                        "alfanumeric_pattern"
                                    ],
                                    "filter":[
                                        "lowercase",
                                        "asciifolding"
                                    ],
                                    "tokenizer":"ngram_tokenizer"
                                },
                                "stemmer_analyzer":{
                                    "tokenizer":"standard",
                                    "filter":[
                                        "lowercase",
                                        "asciifolding",
                                        "stemmer_pt_br"
                                    ]
                                },
                                "stemmer_analyzer_and_mapping":{
                                    "char_filter":[
                                        "mapping_filter"
                                    ],
                                    "tokenizer":"standard",
                                    "filter":[
                                        "lowercase",
                                        "asciifolding",
                                        "stemmer_pt_br"
                                    ]
                                },
                                "alfanumeric_analyzer":{
                                    "char_filter":[
                                        "alfanumeric_pattern"
                                    ],
                                    "filter":[
                                        "lowercase",
                                        "asciifolding",
                                        "leading_zeroes_filter"
                                    ],
                                    "tokenizer":"standard"
                                },
                                "numeric_analyzer":{
                                    "filter":[
                                        "numeric_filter"
                                    ],
                                    "tokenizer":"keyword"
                                },
                                "leading_zeroes_analyzer":{
                                    "filter":[
                                        "leading_zeroes_filter"
                                    ],
                                    "tokenizer":"keyword"
                                },
                                "default":{
                                    "filter":[
                                        "lowercase",
                                        "asciifolding"
                                    ],
                                    "tokenizer":"standard"
                                }
                            }
                        }
                    },
                    "url_idx":str_idx_exp_url,
                    "actv_idx": True
                }
                return self.send_request(self.httppost, url_path=['_txt_idx'],data={self.txt_idx_param: object2json(txt_idx)})