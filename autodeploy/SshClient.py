import paramiko
from common import debug

class SshClient:

    def __init__(self, hostname, username, directory, password=None, sshkey=None):
        self.hostname   = hostname
        self.username   = username
        self.password   = password
        self.sshkey     = sshkey
        self.directory  = directory
        self.connected  = False
        self.timeout    = 2

    def debug(self, msg):
        debug('SshClient: %s' % msg)

    def connect(self):
        if not self.connected:
            self.debug('Connecting to: %s' % self.hostname)
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            if self.sshkey:
                self.ssh.connect(self.hostname, username=self.username, password=None, key_filename=self.sshkey, timeout=self.timeout)
            else:
                self.ssh.connect(self.hostname, username=self.username, password=self.password, timeout=self.timeout)

    def command(self, command):
        self.connect()
        self.debug('Running command: %s' % command)
        chan = self.ssh.get_transport().open_session()
        chan.set_combine_stderr(True)
        chan.exec_command(command)
        exitcode = chan.recv_exit_status()
        stdout = chan.recv(4096)
        if exitcode != 0:
            e = Exception("Error running comand '%s':\n%s" % (command, stdout))
            e.stdout = stdout
            raise e
        return stdout

