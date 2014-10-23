from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError
from sqlalchemy.orm.exc import NoResultFound

from .models import (
    DBSession,
    Secret,
    )

import colander
import datetime
from datetime import timedelta

from .crypto import (
    SecretEncrypter,
    SecretDecrypter,
    )

from Crypto.Hash import SHA256

#toHex = lambda x:"".join([hex(ord(c))[2:].zfill(2) for c in x])
def is_intinrangeor(val, rmin, rmax, become):
    if int(val) < rmin and int(val) > rmax:
        return become
    else:
        return int(val)

def is_valisinchoices(val, choices, become):
    if val in choices:
        return val
    else:
        return become

@view_config(route_name='expired', renderer='templates/expired.pt')
def view_err(request):
    return Response('not found!', content_type='text/plain', status_int=404)

@view_config(route_name='home', renderer='templates/home.pt')
def view_home(request):
    return {}

@view_config(route_name='save', renderer='templates/save.pt')
def view_save(request):
    if not request.method == 'POST':
        return Response('Method not allowed', content_type='text/plain', status_int=405)

    se = SecretEncrypter()
    uid = se.encrypt(request.POST['data'])
    model = se.ret_secret_model()

    choices = ('', 'as3','shell','cf','csharp','cpp','css','delphi','diff','erl',
        'groovy','js','java','jfx','pl','php','plain','ps','py','ruby',
        'scala','sql','vb','xml'
        )

    hours_to_expire = is_intinrangeor(request.POST['maximum_views'], 1, 5, 2)
    model.ExpiryTime = datetime.datetime.now() + timedelta(hours=hours_to_expire)

    model.LifetimeReads = is_intinrangeor(request.POST['hours_until_expiration'], 1, 168, 4)
    model.Snippet = is_valisinchoices(request.POST['snippet_type'], choices, 'plain')

    if len(request.POST['data']) < 1:
        #invalid form (no data to save was given)
        return HTTPFound(location=request.route_url('home'))

    DBSession.add(model)
    return {'uniqid':uid}

@view_config(route_name='retr', renderer='templates/retr.pt')
def view_retr(request):
    if request.method == 'POST':
        return Response('Method not allowed', content_type='text/plain', status_int=405)

    if len(request.matchdict['uniqid']) != 32:
        return Response('Bad request', content_type='text/plain', status_int=400)
    
    session = DBSession()
    uniqid = request.matchdict['uniqid']

    hasher = SHA256.new()
    hasher.update('{}{}'.format(uniqid, uniqid))
    uniqhash = hasher.hexdigest()

    try:
        result = session.query(Secret).\
            filter(Secret.UniqHash == uniqhash,\
                   Secret.ExpiryTime >= datetime.datetime.now(),\
                   Secret.LifetimeReads > 0).one()
    except NoResultFound as e:
        url = request.route_url('expired')
        return HTTPFound(location=url)

    sd = SecretDecrypter()
    data = sd.decrypt_model(result, uniqid )
    session.query(Secret).\
        filter(Secret.UniqHash == uniqhash).\
        update({"LifetimeReads":result.LifetimeReads - 1})

    return {
        'datatype':result.Snippet,
        'views_remain':result.LifetimeReads,
        'time_expires':result.ExpiryTime,
        'data':data,
    }
 
