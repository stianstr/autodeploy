# RemoteBranchChecker
# apt-get install python-paramiko
import paramiko
from common import debug
from SshClient import SshClient

class RemoteBranchChecker(SshClient):

    def debug(self, msg):
        debug('RemoteBranchChecker: %s' % msg)

    def get(self):
        lines = self.command('cd "%s" && git branch' % self.directory)
        branch = self.parseBranchLines(lines)
        if not branch:
            raise Exception("Found no branch in output of 'git branch': %s" % lines)
        self.debug("Remote branch at '%s' is: %s" % (self.hostname, branch))
        return branch

    def parseBranchLines(self, lines):
        for line in lines.split('\n'):
            if line[0] == '*' and line[1] == ' ':
                return line[2:].strip()

    def isMasterBranch(self, branch):
        return branch == 'master'


