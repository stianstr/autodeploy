# Git
# apt-get install python-git
#import git, os
import os, subprocess
from common import debug
from LocalGitBase import LocalGitBase

class BranchDoesNotContainLatestMasterCommit(Exception):
    def __init__(self, latestMasterCommit):
        Exception.__init__(self, 'Branch does not contain latest commit from master')
        self.latestMasterCommit = latestMasterCommit

class BranchContainsMasterChecker(LocalGitBase):

    def debug(self, msg):
        debug('BranchContainsMasterChecker: %s' % msg)

    def check(self, branch):
        self.init(branch)
        commit = self.getLatestMasterCommit()
        self.debug('Last master commit: %s' % commit)
        if not self.checkDeployBranchContainsCommit(commit):
            raise BranchDoesNotContainLatestMasterCommit(commit)

    def getLatestMasterCommit(self):
        result = self.gitCommand(self.masterDirectory, ['log', '-n', '1', "--pretty=format:%H"])
        if not result:
            raise Exception('Could not get last commit for master branch in: %s' % self.masterDirectory)
        return result

    def getLatestDeployBranchCommit(self):
        result = self.gitCommand(self.branchDirectory, ['log', '-n', '1', "--pretty=format:%H"])
        if not result:
            raise Exception('Could not get last commit for deploy branch in: %s' % self.branchDirectory)
        return result

    def checkDeployBranchContainsCommit(self, commit):
        try:
            text = self.gitCommand(self.branchDirectory, ['branch', '--contains', commit])
        except Exception, e:
            if e.message and e.message.find('no such commit'):
                return False
            else:
                raise e
        if not text:
            return False
        for line in text.split('\n'):
            line = line.strip()
            if not line:
                continue
            if line[0] == '*' and line[1] == ' ':
                if line[2:].strip() == self.branch:
                    return True
        return False



