from __future__ import division

from pyramid.response import Response
from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from AppLogging import logger

from sqlalchemy.exc import (
    DBAPIError,
    OperationalError,
    DatabaseError
    )

from sqlalchemy.orm.exc import NoResultFound

from .models import (
    DBSession,
    Secret,
    )

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

@view_config(route_name='expired', renderer='angerona:templates/expired.mak')
def view_err(request):
    return {}

@view_config(route_name='sorry', renderer='angerona:templates/sorry.mak')
def view_sorry(request):
    return {}

@view_config(route_name='home', renderer='angerona:templates/home.mak')
def view_home(request):
    return {}

@view_config(route_name='save', renderer='angerona:templates/save.mak')
def view_save(request):
    if not request.method == 'POST':
        return Response('Method not allowed', content_type='text/plain', status_int=405)

    se = SecretEncrypter()
    logger.debug(request.POST['data'])
    uid = se.encrypt(request.POST['data'])
    model = se.ret_secret_model()

    choices = ('', 'as3','shell','cf','csharp','cpp','css','delphi','diff','erl',
        'groovy','js','java','jfx','pl','php','plain','ps','py','ruby',
        'scala','sql','vb','xml'
        )

    hours_to_expire = is_intinrangeor(request.POST['hours_until_expiration'], 1, 168, 4)
    model.ExpiryTime = datetime.datetime.now() + timedelta(hours=hours_to_expire)

    model.LifetimeReads = is_intinrangeor(request.POST['maximum_views'], 1, 5, 2)
    model.Snippet = is_valisinchoices(request.POST['snippet_type'], choices, 'plain')

    if len(request.POST['data']) < 1:
        #invalid form (no data to save was given)
        return HTTPFound(location=request.route_url('home'))

    friendly_time = '{}d {}h'.format(hours_to_expire // 24, hours_to_expire % 24) 

    session = DBSession()

    try:
        logger.debug("Attempting to save snippet")
        session.add(model)

        logger.debug("Attempting to flush to database")
        session.flush()

    except DBAPIError, exc:
        logger.error("DBAPIError: %s" % exc)
        return HTTPFound(location=request.route_url('sorry'))
        
    return {
        'uniqurl':request.route_url('retr', uniqid=uid),
        'views_remain':model.LifetimeReads,
        'friendly_time':friendly_time,
    }

@view_config(route_name='retr', renderer='angerona:templates/retr.mak')
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
        return HTTPFound(location=request.route_url('expired'))

    sd = SecretDecrypter()
    data = sd.decrypt_model(result, uniqid )
    try:
        session.query(Secret).\
            filter(Secret.UniqHash == uniqhash).\
            update({"LifetimeReads":result.LifetimeReads - 1})
    except Exception, e:
        logger.error("Error updating LifetimeReads value for this snippet: %s" % e)
        pass

    diff = result.ExpiryTime - datetime.datetime.now()
    diff = diff.total_seconds()
    friendly_time = '{}d {}h {}m'.format(int(diff//86400), int(diff//3600), int((diff//60)%60))

    return {
        'datatype':result.Snippet,
        'views_remain':result.LifetimeReads,
        'friendly_time':friendly_time,
        'uniqid':uniqid,
        'data':data,
    }

@view_config(route_name='retrdel', renderer='angerona:templates/expired.mak')
def view_retrdel(request):
    session = DBSession()
    uniqid = request.matchdict['uniqid']

    hasher = SHA256.new()
    hasher.update('{}{}'.format(uniqid, uniqid))
    uniqhash = hasher.hexdigest()

    try:
        session.query(Secret).\
            filter(Secret.UniqHash == uniqhash).\
            delete()
        session.flush()
    except NoResultFound as e:
        pass

    return HTTPFound(location=request.route_url('expired'))
