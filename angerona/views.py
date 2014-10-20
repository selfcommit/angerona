from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

from deform import Form
from deform import ValidationFailure

from .models import (
    DBSession,
    Secret,
    )

import colander

from .crypto import SecretEncrypter

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
    schema = SavePasswordForm()
    pwform = Form(schema, action='/save', buttons=('submit',))
    return {'pwform': pwform.render()}

@view_config(route_name='save', renderer='templates/save.pt')
def view_save(request):
    if not request.method == 'POST':
        return Response('Method not allowed', content_type='text/plain', status_int=405)
    #
    se = SecretEncrypter()
    uid = se.encrypt(request.POST['data'])
    model = se.ret_secret_model()

    DBSession.add(model)

    toHex = lambda x:"".join([hex(ord(c))[2:].zfill(2) for c in x])
    
    return {'uniqid':uid, 'data':toHex(model.CipherText)}
    
@view_config(route_name='retr', renderer='templates/retr.pt')
def view_retr(request):
    if request.method == 'POST':
        return Response('Method not allowed', content_type='text/plain', status_int=405)

    if len(request.matchdict['uniqid']) != 32:
        return Response('Bad request', content_type='text/plain', status_int=400)
    
    session = DBSession()
    themod = session.query(Secret).filter_by(name=request.matchdict['uniqid']).one()
    sd = SecretDecrypter()
    data2 = sd.decrypt_model(themod)

    return Response(data2, content_type='text/plain', status_int=200)
    
