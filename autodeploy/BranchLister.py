from common import debug
from LocalGitBase import LocalGitBase

class BranchLister(LocalGitBase):

    def debug(self, msg):
        debug('BranchList: %s' % msg)

    def list(self):
        self.init('master')
        out = self.gitCommand(self.branchDirectory, ['branch', '-r'])
        return self.parseBranchesLines(out)

    def exists(self, branch):
        branches = self.list()
        return (branch in branches)

    def parseBranchesLines(self, lines):
        branches = []
        for line in lines.split('\n'):
            line = line.strip()
            if not line:
                continue
            if line[0] == '*' and line[1] == ' ':
                line = line[2:]
            if line[:11] == 'origin/HEAD':
                continue
            if line[:7] == 'origin/':
                line = line[7:]
            if line == 'master':
                continue
            branches.append(line)
        return branches


if __name__ == '__main__':
    from DependencyContainer import DependencyContainer
    dc = DependencyContainer()
    b = dc.getBranchLister()
    print b.list()
