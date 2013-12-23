from common import debug
from SshClient import SshClient

class GotUncomittedChanges(Exception):
    def __init__(self, output):
        Exception.__init__(self, 'Server got uncomitted changes')
        self.output = output

class RemoteUncomittedChecker(SshClient):

    def debug(self, msg):
        debug('RemoteUncommittedChecker: %s' % msg)

    def check(self):
        _lines = self.command('cd "%s" && git status' % self.directory)
        if not _lines:
            raise Exception('No output of git status command')

        lines = []
        for line in _lines.split('\n'):
            line = line.strip()
            if not line or line[0] == '#':
                continue
            lines.append(line.strip())

        if len(lines) == 1 and lines[0] == 'nothing to commit (working directory clean)':
            return

        raise GotUncomittedChanges(_lines)


if __name__ == '__main__':

    o = RemoteUncomittedChecker(
        'some.server.com',
        'user', 'password',
        '/srv/myapp'
    )
    o.check()

