from common import debug
from SshClient import SshClient

class AlreadyDeployed(Exception):
    def __init__(self):
        Exception.__init__(self, 'Already deployed')

class Deployer(SshClient):

    def debug(self, msg):
        debug('Deployer: %s' % msg)

    def deploy(self, branch):
        lines = self.command('cd "%s" && git fetch origin' % self.directory)
        lines = self.command('cd "%s" && git checkout %s' % (self.directory, branch))
        if lines and lines.strip() == "Already on '%s'" % branch:
            self.debug(lines)
            raise AlreadyDeployed()
        self.debug(lines)
        lines = self.command('cd "%s" && git pull' % self.direcory)
        self.debug(lines)


if __name__ == '__main__':

    o = Deployer(
        'some.server.com',
        'user', 'password',
        '/srv/myproject'
    )
    o.deploy('some-test-branch')
    #o.deploy('master')

