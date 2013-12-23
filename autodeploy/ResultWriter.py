import os, uuid, json, time

class ResultWriter:

    def __init__(self, datadir):
        self.datadir = datadir
        if not self.datadir:
            raise Exception('Must have datadir')
        if not os.path.exists(self.datadir+'/data'):
            os.makedirs(self.datadir+'/data')

    def write(self, data):
        data['time'] = time.strftime('%Y-%m-%d %H:%M:%S')
        id = self.getNextId()
        self.writeData(id, data)
        self.writeLogs(id, data)
        return id

    def writeData(self, id, data):
        filename = self.getDataFileName(id)
        fp = open(filename, 'w')
        fp.write(json.JSONEncoder().encode(data))
        fp.close()

    def writeLogs(self, id, data):

        filename = self.getAllLogFileName()
        fp = open(filename, 'a')
        result = 'success'
        if not data['result']:
            result = 'fail'
        fp.write('%s\t%-10s\t%-5s\t%-20s\t%-20s\t%-10s\t%s\n' % (data['time'], data['user'], data['type'], data['server'], data['branch'], result, id))
        fp.close()

        if data['type'] == 'deploy' and data['result']:
            filename = self.getDeploySuccessLogFileName()
            fp = open(filename, 'a')
            fp.write('%s\t%-10s\t%-20s\t%-20s\t%s\n' % (data['time'], data['user'], data['server'], data['branch'], id))
            fp.close()

    def getDataFileName(self, id):
        return self.datadir + '/data/' + id + '.json'

    def getAllLogFileName(self):
        return self.datadir + '/all.log'

    def getDeploySuccessLogFileName(self):
        return self.datadir + '/deploy-success.log'

    def getNextId(self):
        return str(uuid.uuid4())

    def load(self, id):
        filename = self.getDataFileName(id)
        fp = open(filename, 'r')
        text = fp.read()
        fp.close()
        return json.JSONDecoder().decode(text)

if __name__ == '__main__':
    o = ResultWriter('/tmp/autodeploy')
    o.write({
        'type':  'check',
        'user':  'user',
        'result': False,
        'branch': 'some-test-branch',
        'server': 'dev-server',
        'build':  {'result': True},
        'lock':   {'result': True},
        'merge':  {'result': False, 'message': 'Branch does not contain latest commit from master'},
        'revision': '5a9db78facd57f402c42e95a95a28c21d9a43c2c'
    })
    o.write({
        'type':  'deploy',
        'user':  'user',
        'result': True,
        'branch': 'some-test-branch',
        'server': 'dev-server',
        'build':  {'result': True},
        'lock':   {'result': True},
        'merge':  {'result': False, 'message': 'Branch does not contain latest commit from master'},
        'revision': '5a9db78facd57f402c42e95a95a28c21d9a43c2c'
    })
