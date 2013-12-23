from common import debug
#from CiServer import *
#from RemoteBranchChecker import RemoteBranchChecker
#from BranchContainsMasterChecker import BranchContainsMasterChecker, BranchDoesNotContainLatestMasterCommit
#from RemoteUncomittedChecker import RemoteUncomittedChecker, GotUncomittedChanges
from CiServer import BuildStatusException
from BranchContainsMasterChecker import BranchDoesNotContainLatestMasterCommit
from RemoteUncomittedChecker import GotUncomittedChanges
import traceback

class DeploymentChecker:

    def __init__(self, ciServer, remoteBranchChecker, branchContainsMasterChecker, remoteUncomittedChecker, branchLister):
        self.ciServer                      = ciServer
        self.remoteBranchChecker           = remoteBranchChecker
        self.branchContainsMasterChecker   = branchContainsMasterChecker
        self.remoteUncomittedChecker       = remoteUncomittedChecker
        self.branchLister                  = branchLister
        self.result                        = {}

    def check(self, branch):

        self.result['type']        = self.checkCorrectBranchType(branch)
        self.result['merge']       = self.checkBranchContainsMaster(branch)
        self.result['revision']    = self.branchContainsMasterChecker.getLatestDeployBranchCommit()
        self.result['uncomitted']  = self.checkRemoteUncomitted()
        self.result['build']       = self.checkBuildStatus(self.result['revision'])
        self.result['lock']        = self.checkDeployedBranchIsMaster()

        self.result['result'] = True
        for key in ['type', 'merge', 'uncomitted', 'build', 'lock']:
            if not self.result[key]['result']:
                self.result['result'] = False

        return self.result

    def checkBuildStatus(self, revision):
        result = {
            'result':      False, 
            'exception':   False,
            'message':     None, 
            'revision':    revision,
            'buildNumber': None, 
            'buildStatus': None,
            'buildLink':   None
        }
        try:
            self.ciServer.checkBuildStatusForRevision(revision)
            result['result'] = True
        except BuildStatusException, e:
            result['message'] = e.message
            result['buildStatus'] = e.buildStatus
            result['buildNumber'] = e.buildNumber
            result['buildLink'] = e.getBuildLink()
        except Exception, e:
            self.exceptionToResult(e, result)
        return result

    def checkDeployedBranchIsMaster(self):
        result = {
            'result':    False, 
            'message':   None, 
            'branch':    None,
            'exception': False
        }
        try:
            remoteBranch = self.remoteBranchChecker.get()
            if self.remoteBranchChecker.isMasterBranch(remoteBranch):
                result['result'] = True
            else:
                result['message'] = 'Server is currently staging another branch: %s' % remoteBranch
                result['branch'] = remoteBranch
        except Exception, e:
            self.exceptionToResult(e, result)
        return result

    def checkBranchContainsMaster(self, branch):
        result = {
            'result':    False,
            'message':   None,
            'exception': False
        }
        try:
            self.branchContainsMasterChecker.check(branch)
            result['result'] = True
        except BranchDoesNotContainLatestMasterCommit, e:
            result['message'] = e.message
            result['latestMasterCommit'] = e.latestMasterCommit
        except Exception, e:
            self.exceptionToResult(e, result)
        return result

    def checkRemoteUncomitted(self):
        result = {
            'result':    False,
            'message':   None,
            'exception': False,
            'changes':   None
        }
        try:
            self.remoteUncomittedChecker.check()
            result['result'] = True
        except GotUncomittedChanges, e:
            result['message'] = e.message
            result['changes'] = e.output
        except Exception, e:
            self.exceptionToResult(e, result)
        return result

    def checkCorrectBranchType(self, branch):
        if not self.branchLister.exists(branch):
            return {
                'result':  False,
                'message': 'No such branch'
            }
        if branch == 'master':
            return {
                'result':  False,
                'message': 'Master branch should not be used directly, only merged into'
            }
        else:
            return {
                'result':  True,
                'message': None
            }

    def exceptionToResult(self, exception, result):
        lines = exception.message.split('\n')
        for line in lines:
            line = line.strip()
            if line:
                result['message'] = line
                break
        #result['exception'] = '%s: %s' % (exception.__class__, exception.message)
        result['exception'] = traceback.format_exc()


if __name__ == '__main__':

    from CiServer import *
    from RemoteBranchChecker import RemoteBranchChecker
    from BranchContainsMasterChecker import BranchContainsMasterChecker, BranchDoesNotContainLatestMasterCommit
    from RemoteUncomittedChecker import RemoteUncomittedChecker, GotUncomittedChanges

    revision  = 'fcf81cc2cc2f51ca008dc03754af9bfe9d19a0aa'
    hostname  = 'some.server.com'
    username  = 'user'
    password  = 'password'
    directory = '/srv/myapp'
    branch    = 'some-test-branch'

    deployer = DeploymentChecker(
        CiServer('http://jenkins.server.com:8080', 'MyProject'),
        RemoteBranchChecker(hostname, username, password, directory),
        BranchContainsMasterChecker('git@somewhere.com:repo/repo.git', '/srv/auto-deploy-data', '/root/.ssh/id_dsa'),
        RemoteUncomittedChecker(hostname, username, password, directory)
    )
    result = deployer.check(branch)

    print ''
    for key,text in [('build','Build status is green'),('lock','Server is not already staging'),('merge','Branch contains latest commit from master')]:
        msg = text
        status = 'OK'
        if not result[key]['result']:
            status = 'ERROR'
            msg = result[key]['message']
        print '%-8s %s' % (status, msg)

    print ''
    print 'DETAILS:'
    import pprint
    pprint.pprint(result)
    print ''

