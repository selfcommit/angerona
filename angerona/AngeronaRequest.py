from pyramid.request import Request
from pyramid.decorator import reify
from uuid import uuid4


class AngeronaRequest(Request):
    @reify
    def id(self):
        return str(uuid4())

