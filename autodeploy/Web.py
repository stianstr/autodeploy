from bottle import route, run, template, static_file, request, auth_basic
import os
import Api
from DependencyContainer import DependencyContainer
import json

dir = os.path.dirname(os.path.realpath(__file__))

resultWriter = DependencyContainer().getResultWriter()
users        = DependencyContainer().config['web']['users']
currentUser  = None

def getLastLogData(file):
    if not os.path.exists(file):
        return []
    f = open(file, 'r')
    lines = f.readlines()
    f.close()
    result = []
    for line in lines[-10:]:
        item = []
        for value in line.split('\t'):
            item.append(value.strip())
        result.append(item)
    result.reverse()
    return result

def getLastLogAll():
    return getLastLogData(resultWriter.getAllLogFileName())

def getLastLogDeploySuccess():
    return getLastLogData(resultWriter.getDeploySuccessLogFileName())

def auth_check(user, password):
    for _user in users:
        if _user[0] == user and _user[1] == password:
            currentUser = _user[0]
            return True
    return False

@route('/')
@auth_basic(auth_check)
def index():
    data = {
        'logAll':           getLastLogAll(),
        'logDeploySuccess': getLastLogDeploySuccess(),
        'showDetails':      None,
        'highlight':        None,
        'servers':          Api.getServers(),
        'branches':         Api.getBranches()
    }
    if request.query.show:
        data['showDetails'] = request.query.show
        data['highlight'] = request.query.show
    if request.query.highlight:
        data['highlight'] = request.query.highlight
    return template('templates/index', data=data)

@route('/show/<id>')
@auth_basic(auth_check)
def show(id):
    container = DependencyContainer()
    writer = container.getResultWriter()
    data = writer.load(id)
    data['id'] = id
    data['raw'] = json.dumps(data, indent=2) 
    if request.query.headless and request.query.headless != '0' and request.query.headless != 0:
        data['headless'] = True
    else:
        data['headless'] = False
    return template('templates/show', data=data)

@route('/check/<server>/<branch>')
@auth_basic(auth_check)
def check(server, branch):
    result = Api.check(branch, server, currentUser)
    return json.dumps(result)

@route('/deploy/<server>/<branch>')
@auth_basic(auth_check)
def deploy(server, branch):
    result = Api.deploy(branch, server, currentUser)
    return json.dumps(result)

@route('/merge/<server>/<branch>')
@auth_basic(auth_check)
def merge(server, branch):
    result = Api.merge(branch, server, currentUser)
    return json.dumps(result)

@route('/servers')
@auth_basic(auth_check)
def servers():
    result = []
    servers = Api.getServers()
    for server in servers:
        result.append({
            'alias':    server['alias'],
            'hostname': server['hostname'],
            'branch':   server['branch']
        })
    return json.dumps(result)

@route('/branches')
@auth_basic(auth_check)
def branches():
    branches = Api.getBranches()
    return json.dumps(branches)

@route('/static/<path:path>')
@auth_basic(auth_check)
def callback(path):
    return static_file(path, root=dir + '/static')

@route('/help/<topic>')
@auth_basic(auth_check)
def help_topic(topic):
    data = {}
    if request.query.headless and request.query.headless != '0' and request.query.headless != 0:
        data['headless'] = True
    else:
        data['headless'] = False
    return template('templates/help-%s' % topic, data=data)
    

if __name__ == '__main__':
    config = DependencyContainer().config 
    run(host=config['web']['host'], port=config['web']['port']) #, reloader=True)
