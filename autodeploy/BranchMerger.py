from common import debug
from LocalGitBase import LocalGitBase

class BranchMerger(LocalGitBase):

    def debug(self, msg):
        debug('BranchMerger: %s' % msg)

    def merge(self, branch):
        self.init(branch)
        self.switchBranch(self.branchDirectory, branch)
        self.gitCommand(self.branchDirectory, ['branch', '-D', 'master'], acceptExitCodes=[0,1])
        self.switchBranch(self.branchDirectory, 'master')
        result = self.gitCommand(self.branchDirectory, ['pull'])
        self.debug('PULL: %s' % result)
        result = self.gitCommand(self.branchDirectory, ['merge', '--no-ff', branch])
        self.debug('MERGE: %s' % result)
        result = self.gitCommand(self.branchDirectory, ['push', 'origin', 'master'])
        self.debug('PUSH: %s' % result)
        result = self.gitCommand(self.branchDirectory, ['branch', '-d', branch])
        self.debug('DEL-L: %s' % result)
        result = self.gitCommand(self.branchDirectory, ['push', 'origin', ':%s' % branch])
        self.debug('DEL-R: %s' % result)


