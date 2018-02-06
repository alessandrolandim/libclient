import json

class TypeBase(object):
    """
    Base class for all lbtypes
    """
    def get_dict(self):
        """
        Returns object as a dict that follows LB's REST format.
        Some subclasses override this method.
        """
        d = dict()

        for key, value in self.__dict__.items():
            if isinstance(value, TypeBase):
                value = value.get_dict()
            elif isinstance(value, list):
                value_list = []
                for elem in value:
                    if isinstance(elem, TypeBase):
                        elem = elem.get_dict()
                    value_list.append(elem)
                value = value_list
            d[key] = value

        return d

    def get_json(self):
        """
        Returns JSON representation of the object that follows LB's REST format.
        """
        return json.dumps(self, cls=JSONEncoder)

    @classmethod
    def from_dict(cls, args):
        """
        Creates a new instance of the class from a dictionary (dict object).
        Must be implemented in all subclasses.
        """
        raise NotImplementedError()


class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        get_dict = getattr(obj, 'get_dict', None)

        if get_dict is not None:
            return get_dict()

        return JSONEncoder.default(self, obj)
