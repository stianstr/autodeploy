from DependencyContainer import DependencyContainer
from Deployer import AlreadyDeployed
import traceback

dc = DependencyContainer()

# Step 1 - Check if branch can be deployed
def check(branch, server, user, internalCheck=False):
    checker = dc.getDeploymentChecker(server)
    result = checker.check(branch)
    if not internalCheck:
        result = {'check': result, 'result': result['result']}
        result['id'] = writeResult('check', branch, server, result, user)
    return result

# Step 2 - Deploy branch (then observe if everything is ok)
def deploy(branch, server, user):
    result = {}
    try:
        checkDetails = check(branch, server, user, internalCheck=True)
        if not checkDetails['result']:
            result = {
                'result':    False, 
                'message':   'Check failed',
                'check':     checkDetails,
                'exception': None
            }
        else:
            deployer = dc.getDeployer(server)
            try:
                deployer.deploy(branch)
                result = {
                    'result':    True,
                    'msesage':   'Deployed',
                    'exception': None,
                    'check':    checkDetails
                }
            except AlreadyDeployed, e:
                result = {
                    'result':    False,
                    'message':   'Already deployed',
                    'exception': None,
                    'check':   {}
                }
    except Exception, e:
        result = {
            'result':    False,
            'message':   e.message,
            'exception': traceback.format_exc(),
            'check':     {}
        }
    result['id'] = writeResult('deploy', branch, server, result, user)
    return result

# Step 3 - Merge branch into master and switch server to master
def merge(branch, server, user):
    # todo: sanity-check

    lister = dc.getBranchLister()
    if not lister.exists(branch):
        result = {'check': {}, 'result': False, 'message': 'No such branch'}

    else:

        try:
            merger = dc.getBranchMerger()
            merger.merge(branch)

            deployer = dc.getDeployer(server)
            deployer.deploy('master')

            result = {'check': {}, 'result': True}
        except Exception, e:
            result = {'check': {}, 'result': False}
            _exceptionToResult(e, result)

    result['id'] = writeResult('merge', branch, server, result, user)

    return result

# meh, duplicated elsewhere
def _exceptionToResult(exception, result):
    lines = exception.message.split('\n')
    for line in lines:
        line = line.strip()
        if line:
            result['message'] = line
            break
    #result['exception'] = '%s: %s' % (exception.__class__, exception.message)
    result['exception'] = traceback.format_exc()


def getServers():
    servers = dc.config['servers']
    for server in servers:
        try:
            bc = dc.getRemoteBranchChecker(server['alias'])
            server['branch'] = bc.get()
        except Exception, e:
            server['branch'] = '(%s)' % e.message
    return servers

def getBranches():
    bl = dc.getBranchLister()
    return bl.list()

def writeResult(type, branch, server, data, user):
    data['user'] = user
    data['type'] = type
    data['branch'] = branch
    data['server'] = server
    print 'DATA: %s' % data
    o = dc.getResultWriter()
    return o.write(data)
