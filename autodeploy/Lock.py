import uuid, os

class Lock:

    def lock(self):
        if self.check():
            return False
        id = str(uuid.uuid4())
        self._writeFile(self._getFile(), id)
        return id

    def unlock(self, id):
        id2 = self._readFile(self._getFile())
        if id2 != id:
            raise Exception("Lock ID mismatch. Yours: %s Theirs: %s" %(id, id2))
        self._delFile(self._getFile())

    def check(self):
        data = self._readFile(self._getFile())
        if data:
            return True
        else:
            return False

    def _getFile(self):
        return '/srv/autodeploy/data/work/lock'

    def _writeFile(self, file, data):
        fp = open(file,'w')
        fp.write(data)
        fp.close()

    def _readFile(self, file):
        if os.path.exists(file):
            fp = open(file,'r')
            data = fp.read()
            fp.close()
            return data
        else:
            return None

    def _delFile(self, file):
        os.unlink(file)
    
if __name__ == '__main__':
    l = Lock()
    print 'is-locked(1): %s' % l.check()
    id = l.lock()
    print 'lock: %s' % id
    print 'is-locked(1): %s' % l.check()
    print 'unlock: %s' % l.unlock(id)
    print 'is-locked(1): %s' % l.check()
    
    
