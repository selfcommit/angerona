from pyramid.config import Configurator
from sqlalchemy import engine_from_config
from AngeronaRequest import AngeronaRequest
import ThreadTween
from pyramid.events import NewRequest
from AngeronaMaintenance import CleanupDatabase

from .models import (
    DBSession,
    Base,
    )

def setup_post_request(event):
    event.request.add_finished_callback(CleanupDatabase)



def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('save', '/save')
    config.add_route('retr', '/retr/{uniqid}')
    config.add_route('retrdel', '/retr/{uniqid}/delete')
    config.add_route('expired', '/expired')
    config.add_route('sorry', '/sorry')
    #Log request id with the logger calls
    config.add_subscriber(setup_post_request, NewRequest)
    config.set_request_factory(AngeronaRequest)
    config.add_tween('angerona.ThreadTween.hack_thread_name_tween_factory')

    config.scan()
    return config.make_wsgi_app()
