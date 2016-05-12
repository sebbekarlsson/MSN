import time
import json


class DBObject(object):
    """This class defines how objects in the mongoDB should be represented."""

    def __init__(
            self,
            classes=[],
            type='',
            meta={}
            ):
        self.created = time.strftime("%Y/%B/%d|%H:%M:%S")
        self.updated = time.strftime("%Y/%B/%d|%H:%M:%S")
        self.classes = classes
        self.type = type
        self.meta = meta
        self.structure = '{}{}'.format('#', self.__class__.__name__)


    def export(self):
        """This function exports the object as a dict. This is used when
        putting an object in the database."""

        return self.__dict__


class Post(DBObject):

    def __init__(
            self,
            title='',
            content='',
            attachments=[],
            author={},
            tags=[],
            published='',
            *args,
            **kwargs
            ):
        DBObject.__init__(self, *args, **kwargs)
        self.title = title
        self.content = content
        self.attachments = attachments
        self.author = author
        self.tags = tags
        self.published = published


class User(DBObject):

    def __init__(
            self,
            firstname='',
            lastname='',
            email='',
            password='',
            avatar='',
            token='',
            contacts=[],
            *args,
            **kwargs
            ):
        DBObject.__init__(self, *args, **kwargs)
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = password
        self.avatar = avatar
        self.token = token
        self.contacts = contacts


class Option(DBObject):

    def __init__(
            self,
            key='',
            value='',
            editable=True,
            *args,
            **kwargs
            ):
        DBObject.__init__(self, *args, **kwargs)
        self.key = key
        self.value = value
        self.editable = editable


class File(DBObject):

    def __init__(
            self,
            filename='',
            *args,
            **kwargs
            ):
        DBObject.__init__(self, *args, **kwargs)
        self.filename = filename
