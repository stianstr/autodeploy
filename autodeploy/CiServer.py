# CiServer
# easy_install jenkinsapi  -- NOT the same as apt-get install python-jenkins
from jenkinsapi.jenkins import Jenkins
from common import debug

class BuildStatusException(Exception):
    def __init__(self, message):
        self.revision    = None
        self.buildNumber = None
        self.buildStatus = None
        debug('%s: %s' % (self.__class__, message))
        Exception.__init__(self, message)
    def getBuildLink(self):
        if self.buildNumber:
            return 'http://victor.dev.kq.no:8080/job/Victor/%s/' % self.buildNumber

class BuildRunning(BuildStatusException):
    def __init__(self, revision, buildNumber):
        BuildStatusException.__init__(self, 'Revision is currently being built')
        self.revision = revision
        self.buildNumber = buildNumber

class NoSuchBuild(BuildStatusException):
    def __init__(self, revision):
        BuildStatusException.__init__(self, 'Revision is not built yet')
        self.revision = revision

class BuildIsNotGreen(BuildStatusException):
    def __init__(self, revision, buildStatus, buildNumber):
        BuildStatusException.__init__(self, 'Revision build status is %s' % buildStatus)
        self.revision = revision
        self.buildStatus = buildStatus
        self.buildNumber = buildNumber


class CiServer:

    def __init__(self, url, jobName):
        self.url = url
        self.jobName = jobName

    def debug(self, msg):
        debug('CiServer: %s' % msg)

    def checkBuildStatusForRevision(self, revision):
        status, buildNumber = self.getBuildStatusForRevision(revision)
        if not self.isBuildStatusOk(status):
            raise BuildIsNotGreen(revision, status, buildNumber)

    def getBuildStatusForRevision(self, revision):
        self.debug('Connect to Jenkins at: %s' % self.url)
        jenkins = Jenkins(self.url)

        self.debug('Get job: %s' % self.jobName)
        job = jenkins.get_job(self.jobName)

        self.debug('Get build number for revision: %s' % revision)
        buildNumbers = job.get_buildnumber_for_revision(revision)

        if buildNumbers:

            for buildNumber in buildNumbers:

                self.debug('Get build info for build number: %s' % buildNumber)
                build = job.get_build(buildNumber)

                if build:
                    if build.is_running():
                        raise BuildRunning(revision, buildNumber)
                    else:
                        return (build.get_status(), buildNumber)
                else:
                    raise Exception('No build info for buildNumber=%s revision=%s' % (buildNumber, revision))

        else:
            raise NoSuchBuild(revision)

    def isBuildStatusOk(self, status):
        return status == 'SUCCESS'


if __name__ == '__main__':
    ci = CiServer(
        'http://jenkins.mydomain.com:8080',
        'MyProject'
    )
    status, buildNo = ci.getBuildStatusForRevision('fcf81cc2cc2f51ca008dc03754af9bfe9d19a0aa')
    print 'STATUS: %s' % status
    ok = ci.isBuildStatusOk(status)
    print 'OK: %s' % ok
