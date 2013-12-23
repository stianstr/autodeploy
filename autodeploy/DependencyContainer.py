import json, os

from DeploymentChecker import DeploymentChecker
from Deployer import Deployer
from CiServer import CiServer
from RemoteBranchChecker import RemoteBranchChecker
from BranchContainsMasterChecker import BranchContainsMasterChecker
from BranchMerger import BranchMerger
from BranchLister import BranchLister
from RemoteUncomittedChecker import RemoteUncomittedChecker
from ResultWriter import ResultWriter

class DependencyContainer:

    def __init__(self):
        self.loadConfig(self.getConfigFile())

    def loadConfig(self, file):
        fp = open(file, 'r')
        text = fp.read()
        fp.close()
        data = json.JSONDecoder().decode(text)
        self.config = data

    def getConfigFile(self):
        files = [
            '/etc/autodeploy.json',
            os.path.dirname(os.path.realpath(__file__)) + '/config.local.json',
            os.path.dirname(os.path.realpath(__file__)) + '/config.json'
        ]
        for f in files:
            if os.path.exists(f):
                return f
        raise Exception('No config file found')

    def getServerConfig(self, serverAlias):
        for server in self.config['servers']:
            if server['alias'] == serverAlias:
                return server
        if not server.has_key('sshkey'):
            server['sshkey'] = None
        if not server.has_key('password'):
            server['password'] = None
        raise Exception('No such server: %s' % serverAlias)

    def getCiServer(self):
        return CiServer(
            self.config['jenkins']['url'],
            self.config['jenkins']['project']
        )

    def getRemoteBranchChecker(self, serverAlias):
        server = self.getServerConfig(serverAlias)
        return RemoteBranchChecker(
            hostname=server['hostname'],
            username=server['username'],
            password=server['password'],
            sshkey=server['sshkey'],
            directory=server['directory']
        )

    def getRemoteUncomittedChecker(self, serverAlias):
        server = self.getServerConfig(serverAlias)
        return RemoteUncomittedChecker(
            hostname=server['hostname'],
            username=server['username'],
            password=server['password'],
            sshkey=server['sshkey'],
            directory=server['directory']
        )

    def getBranchContainsMasterChecker(self):
        return BranchContainsMasterChecker(
            self.config['git']['url'],
            self.config['git']['workdir'],
            self.config['git']['sshkey']
        )

    def getBranchMerger(self):
        return BranchMerger(
            self.config['git']['url'],
            self.config['git']['workdir'],
            self.config['git']['sshkey']
        )

    def getBranchLister(self):
        return BranchLister(
            self.config['git']['url'],
            self.config['git']['workdir'],
            self.config['git']['sshkey']
        )

    def getDeploymentChecker(self, serverAlias):
        return DeploymentChecker(
            self.getCiServer(),
            self.getRemoteBranchChecker(serverAlias),
            self.getBranchContainsMasterChecker(),
            self.getRemoteUncomittedChecker(serverAlias),
            self.getBranchLister()
        )

    def getDeployer(self, serverAlias):
        server = self.getServerConfig(serverAlias)
        return Deployer(
            hostname=server['hostname'],
            username=server['username'],
            password=server['password'],
            sshkey=server['sshkey'],
            directory=server['directory']
        )

    def getResultWriter(self):
        return ResultWriter(self.config['result']['datadir'])
            


if __name__ == '__main__':
    import pprint
    o = DependencyContainer()
    pprint.pprint(o.config)
    
