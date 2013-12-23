import os, subprocess
from common import debug

class LocalGitBase:

    def __init__(self, repositoryAddress, temporaryDirectory, sshPrivateKey):
        self.repositoryAddress = repositoryAddress
        self.baseDirectory     = temporaryDirectory + '/repos'
        self.masterDirectory   = self.baseDirectory + '/master'
        self.sshPrivateKey     = sshPrivateKey
        self.branchDirectory   = None
        self.branch            = None

    def debug(self, msg):
        debug('RevisionContainsMasterChecker: %s' % msg)

    def init(self, branch):
        self.makeGitSshWrapper()
        self.setDeployBranch(branch)
        self.initRepositories()

    def initRepositories(self):
        for directory in [self.masterDirectory, self.branchDirectory]:
            self.ensureDirectoryExists(directory)
            self.ensureDirectoryIsCloned(directory)
        self.ensureDirectoryHasBranch(self.masterDirectory, 'master')
        self.ensureDirectoryHasBranch(self.branchDirectory, self.branch)
        self.pull(self.masterDirectory) #, 'master')
        self.pull(self.branchDirectory) #, self.branch)

    def setDeployBranch(self, branch):
        self.branch = branch
        self.branchDirectory = self.baseDirectory + '/' + branch


    def ensureDirectoryExists(self, directory):
        if not os.path.exists(directory):
            self.debug('Creating directory: %s' % directory)
            os.makedirs(directory)

    def ensureDirectoryIsCloned(self, directory):
        if not self.isDirectoryCloned(directory):
            self.cloneToDirectory(directory)

    def cloneToDirectory(self, directory):
        self.gitCommand(directory, ['clone', self.repositoryAddress, '.'])

    def isDirectoryCloned(self, directory):
        return os.path.exists(directory + '/.git')

    def getDirectoryBranch(self, directory):
        result = self.gitCommand(directory, ['branch'])
        if not result:
            raise Exception('No result from git branch command')
        branch = self.parseBranchLines(result)
        if not branch:
            raise Exception('Found no current branch in output of git branch command')
        return branch

    def parseBranchLines(self, text):
        for line in text.split('\n'):
            if line[0] == '*' and line[1] == ' ':
                return line[2:].strip()

    def ensureDirectoryHasBranch(self, directory, wantedBranch):
        currentBranch = self.getDirectoryBranch(directory)
        if currentBranch == wantedBranch:
            self.debug('Directory: %s already has branch: %s' % (directory, wantedBranch))
            return
        self.debug('Switching to branch: %s for directory: %s' % (wantedBranch, directory))
        self.switchBranch(directory, wantedBranch)

    def switchBranch(self, directory, branch):
        self.gitCommand(directory, ['checkout', branch])

    def pull(self, directory): #, branch):
        self.gitCommand(directory, ['pull']) #, 'origin', branch])

    def makeGitSshWrapper(self):
        baseDirectory = self.baseDirectory + '/gitssh'
        self.debug('makeGitSshWrapper: dir = %s' % baseDirectory)
        if not os.path.exists(baseDirectory):
            os.makedirs(baseDirectory)
        self.sshWrapperScript = baseDirectory + '/gitssh.sh'
        f = open(self.sshWrapperScript, 'w')
        f.write('ssh -i %s $@' % self.sshPrivateKey)
        f.close()
        os.chmod(self.sshWrapperScript, 0755)

    def gitCommand(self, directory, command, acceptExitCodes=None):
        command2 = ['git'] #, '--git-dir', directory]
        for part in command:
            command2.append(part)
        return self.command(command2, cwd=directory, acceptExitCodes=acceptExitCodes)

    def command(self, command, cwd=None, acceptExitCodes=None):
        env={'GIT_SSH':self.sshWrapperScript}
        self.debug('CMD: %s @ %s - ENV: %s' % (command, cwd, env))
        p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd, env=env)
        stdout, stderr = p.communicate()
        exitcode = p.wait()
        if (acceptExitCodes and exitcode in acceptExitCodes) or exitcode == 0:
            return stdout
        raise Exception('%s\n\n%s\n\nCommand: %s\n\nExit-code: %s\n' % (stdout, stderr, command, exitcode))


