from ..lbtypes import TypeBase


class Field(TypeBase):
    """
    Represents a field and its metadata in a base
    """
    def __init__(self, name, datatype, alias='', description='',
                 required=False, multivalued=False, indices=None):
        """
        Class initializer.
        """
        self.name = name
        self.datatype = datatype
        self.alias = alias
        self.description = description
        self.required = required
        self.multivalued = multivalued
        if indices is None:
            if self.datatype in ['File', 'Document', 'Sound',
                                 'Video', 'Image']:
                self.indices = ["Textual"]
            else:
                self.indices = ["Textual", "Ordenado"]
        else:
            self.indices = indices

    def get_dict(self):
        """
        Returns field as a dict that follows LB's REST format.
        """
        return {'field': super(Field, self).get_dict()}

    @classmethod
    def from_dict(cls, args):
        """
        Creates a new Field object from a dictionary (dict object)
        """
        if not isinstance(args, dict):
            raise TypeError('Wrong parameter: not a dictionary')

        field = cls(args['name'], args['datatype'])

        for key, value in args.items():
            setattr(field, key, value)


class GroupMetadata(TypeBase):
    """
    Represents a Group's metadata
    """
    def __init__(self, name, alias='', description='', multivalued=False):
        if name is None:
            raise TypeError('Wrong parameter: name must be a string')

        self.name = name
        self.alias = alias
        self.description = description
        self.multivalued = multivalued

    @classmethod
    def from_dict(cls, args):
        """
        Creates a new GroupMetadata object from a dictionary (dict object)
        """
        if not isinstance(args, dict):
            raise TypeError('Wrong parameter: not a dictionary')

        metadata = GroupMetadata(args.get('name', None))

        for k, v in args.items():
            setattr(metadata, k, v)

        return metadata


class Group(TypeBase):
    """
    Represents a Group in a base
    """
    def __init__(self, metadata=None, content=None, **kwargs):
        """
        Must provide either a GroupMetadata object or named parameters containing
        metadata fields.
        (Only 'name' field is required, see GroupMetadata class for default values)
        
        Ex 1: group = Group(metadata=GroupMetadata(name='group_name', required=True))
        Ex 2: group = Group(name='group_name', required=True)
        Examples 1 and 2 produce the same result.
        """
        if metadata is None:
            self.metadata = GroupMetadata(**kwargs)
        elif isinstance(metadata, GroupMetadata):
            self.metadata = metadata
        else:
            raise TypeError('Wrong parameter: metadata must be GroupMetadata ' + \
                'or args must be provided')
        
        self.content = content or []

    def add_field(self, field):
        """
        Add a Field or Group to this group.

        @param field (Field or Group): the field (libclient.lbtypes.base.Field) or 
            group (libclient.lbtypes.base.Group) to be added
        """
        if not (isinstance(field, Field) or isinstance(field, Group)):
            raise TypeError('Wrong parameter: field must be a Field or Group')

        self.content.append(field)

    def get_dict(self):
        """
        Returns group as a dict that follows LB's REST format.
        """
        return {'group': super(Group, self).get_dict()}

    @classmethod
    def from_dict(cls, args):
        """
        Creates a new Group object from a dictionary (dict object)
        """
        if not isinstance(args, dict):
            raise TypeError('Wrong parameter: not a dictionary')

        group = cls(name=args['metadata']['name'])

        for key, value in args.items():
            if not key == 'content' and not key == 'metadata':
                setattr(group, key, value)

        group.metadata = GroupMetadata.from_dict(args['metadata'])

        for c in args['content']:
            for key, value in c.items():
                if key == 'field':
                    obj = Field.from_dict(value)

            if obj is not None:
                group.add_field(obj)

        return group


class BaseMetadata(TypeBase):
    """
    Represents a Base's metadata
    """
    def __init__(self, name, description='', password='', color='',
        idx_exp=False, idx_exp_url='', idx_exp_time='0', file_ext=False,
        file_ext_time='0'):
        if name is None:
            raise TypeError('Wrong parameter: name must be a string')

        self.name = name
        self.description = description
        self.password = password
        self.color = color
        self.idx_exp = idx_exp
        self.idx_exp_url = idx_exp_url
        self.idx_exp_time = idx_exp_time
        self.file_ext = file_ext
        self.file_ext_time = file_ext_time


    @classmethod
    def from_dict(cls, args):
        """
        Creates a new Metadata object from a dictionary (dict object)
        """
        if not isinstance(args, dict):
            raise TypeError('Wrong parameter: args must be a dict')

        metadata = BaseMetadata(args['name'])

        for k, v in args.items():
            setattr(metadata, k, v)

        return metadata


class Base(TypeBase):
    def __init__(self, metadata=None, content=None, **kwargs):
        """
        Must provide either a BaseMetadata object or named parameters containing
        metadata fields.
        (Only 'name' field is required, see BaseMetadata class for default values)
        
        Ex 1: base = Base(metadata=BaseMetadata(name='base_name', description='description'))
        Ex 2: group = Base(name='base_name', description='description')
        Examples 1 and 2 produce the same result.
        """

        if metadata is None:
            self.metadata = BaseMetadata(**kwargs)
        elif isinstance(metadata, BaseMetadata):
            self.metadata = metadata
        else:
            raise TypeError('Wrong parameter: metadata must be BaseMetadata ' + \
                'or args must be provided')

        self.content = content or []

    def add_field(self, field):
        """
        Add a Field or Group to the Base.

        @param field (Field or Group): the field (libclient.lbtypes.base.Field) or 
            group (libclient.lbtypes.base.Group) to be added
        """
        if not (isinstance(field, Field) or isinstance(field, Group)):
            raise TypeError('Wrong parameter: not a Field or Group')

        self.content.append(field)

    @classmethod
    def from_dict(cls, args):
        """
        Creates a new Base object from a dictionary (dict object)
        """
        if not isinstance(args, dict):
            raise TypeError('Wrong parameter: not a dictionary')

        base = cls(name=args['metadata']['name'])

        for key, value in args.items():
            if not key == 'content' and not 'metadata':
                setattr(base, key, value)

        base.metadata = BaseMetadata.from_dict(args['metadata'])

        for c in args['content']:
            for key, value in c.items():
                if key == 'field':
                    obj = Field.from_dict(value)
                elif key == 'group':
                    obj = Group.from_dict(value)

                if obj is not None:
                    base.add_field(obj)

        return base


