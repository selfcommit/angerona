from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

import colander
from deform import Form
from deform import ValidationFailure

from .models import (
    DBSession,
    Secret,
    )

class SavePasswordForm(colander.MappingSchema):
    data = colander.SchemaNode(colander.String())
    maximum_views = colander.SchemaNode(
        colander.Integer(),
        validator=colander.Range(1, 5),
        default=2
    )
    hours_until_expiration = colander.SchemaNode(
        colander.Integer(),
        validator=colander.Range(1, 120),
        default=4
    )
    snippet_type = colander.SchemaNode(
        colander.String(),
        validator=colander.OneOf(['Password','Plaintext']),
        default='Password'
    )

@view_config(route_name='home', renderer='templates/home.pt')
def view_home(request):
    #try:
    #    one = DBSession.query(Secret).first()
    #except DBAPIError:
    #    return Response(conn_err_msg, content_type='text/plain', status_int=500)
    #return {'one': one, 'project': 'angerona'}
    schema = SavePasswordForm()
    pwform = Form(schema, buttons=('submit',))
    return {'pwform': pwform.render()}

conn_err_msg = "conn_err"

