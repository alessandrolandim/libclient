from ..lbtypes import TypeBase

class File(TypeBase):
    def __init__(self, id_file=None, id_doc=None, filename=None, filesize=None, \
            mimetype=None, filetext=None, dt_ext_text=None, download=None, content=None):
        self.id_file = id_file
        self.id_doc = id_doc
        self.filename = filename
        self.filesize = filesize
        self.mimetype = mimetype
        self.filetext = filetext
        self.dt_ext_text = dt_ext_text
        self.download = download
        self.content = content


    @classmethod
    def open(cls, file_path):
        if not isinstance(file_path, PYSTR):
            raise TypeError('Wrong parameter: file_path must be a string')

        filename = file_path.split('/')[-1]

        f = open(file_path, 'rb')
        import os
        size = os.fstat(f.fileno()).st_size
        content = f.read()
        f.close()

        file = cls(filename=filename, filesize=size, content=content)
        return file
        

    @classmethod
    def from_dict(cls, args):
        """
        Creates a new File object from a dictionary (dict object)
        """
        if not isinstance(args, dict):
            raise TypeError('Wrong parameter: not a dictionary')

        file = cls(**args)

        return file