from pyramid.response import Response
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError

import deform
from deform import Form
from deform import ValidationFailure

from .models import (
    DBSession,
    Secret,
    )

import colander

from .crypto import (
    SecretEncrypter,
    SecretDecrypter,
    )

from Crypto.Hash import SHA256

#toHex = lambda x:"".join([hex(ord(c))[2:].zfill(2) for c in x])

class SavePasswordForm(colander.MappingSchema):
    mvchoices = (
        ('', '- Number Total -'),
        (1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')
        )
    maximum_views = colander.SchemaNode(
        colander.Integer(),
        validator=colander.Range(1, 5),
        default=2,
        widget=deform.widget.SelectWidget(values=mvchoices)
    )
    huechoices = (
        ('', '- Hours/Days -'),
        (1, '1h'),(2, '2h'),(4, '4h'),(8, '8h'),
        (12, '12h'),(16, '16h'),(20, '20h'),(24, '1d'),
        (36, '1d 12h'),(48, '2d'), (60, '2d 12h'),
        (72, '3d'),(84, '3d 12h'),(96, '4d'),(108, '4d 12h'),
        (120, '5d'),(144, '6d'),(168, '1w')
        )
    hours_until_expiration = colander.SchemaNode(
        colander.Integer(),
        validator=colander.Range(1, 168),
        default=4,
        widget=deform.widget.SelectWidget(values=huechoices)
    )
    dtchoices = (
        ('', 'Password'),
        ('as3', 'ActionScript3'),
        ('shell', 'Bash/Shell'),
        ('cf', 'ColdFusion'),
        ('csharp', 'C#'),
        ('cpp', 'C/C++'),
        ('css', 'CSS'),
        ('delphi', 'Delphi, Pascal'),
        ('diff', 'Diff/Patch'),
        ('erl', 'Erlang'),
        ('groovy', 'Groovy'),
        ('js', 'JavaScript'),
        ('java', 'Java'),
        ('jfx', 'JavaFX'),
        ('pl', 'Perl'),
        ('php', 'PHP'),
        ('ps', 'PowerShell'),
        ('py', 'Python'),
        ('ruby', 'Ruby'),
        ('ps', 'PowerShell'),
        ('scala', 'Scala'),
        ('sql', 'SQL'),
        ('vb', 'Visual Basic'),
        ('xml', 'XML,HTML,XML,XSLT'),
        )
    snippet_type = colander.SchemaNode(
        colander.String(),
        validator=colander.OneOf([(i[0]) for i in dtchoices]),
        default='',
        widget=deform.widget.SelectWidget(values=dtchoices,css_class="datatype")
    )
    data = colander.SchemaNode(
        colander.String()
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

    se = SecretEncrypter()
    uid = se.encrypt(request.POST['data'])
    model = se.ret_secret_model()

    tmp = Form(SavePasswordForm())
    try:
        tmp = tmp.validate(request.POST.items())
    except deform.ValidationFailure as e:
        #invalid form; set everything default & carry on (no redos on this system)
        model.Snippet = ''
        model.ExpiryTime = 4
        model.LifetimeReads = 2

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

    result = session.query(Secret).filter_by(UniqHash=uniqhash).one()
    sd = SecretDecrypter()
    data = sd.decrypt_model(result, uniqid )

    return {
        'datatype':result.Snippet,
        'views_remain':result.LifetimeReads,
        'time_expires':result.ExpiryTime,
        'data':data,
    }
 
