
import sys, urllib2, urllib

from BaseObject import BaseObject


class Process(BaseObject):
    def __init__(self, accept, username="", password="", uid="", process_id="", audioFilename="", metadataFilename="", transcriptFilename="",
                 service=None, item_id=None, count=None):
        BaseObject.__init__(self, accept, username=username, password=password, uid=uid, process_id=process_id,
                            audioFilename=audioFilename, metadataFilename=metadataFilename, transcriptFilename=transcriptFilename,
                            service=service, item_id=item_id, count=count)
        self.path = 'media/'

    @BaseObject._reset_headers
    def get(self):
        print >> sys.stderr, 'making get request to: %s%s' % (self.dest,self.path+self.uid+self.path_trans+self.process_id)
        request = urllib2.Request(self.dest+self.path+self.uid+self.path_trans+self.process_id, headers=self.headers)
        BaseObject._execute(self, request)

    @BaseObject._reset_headers
    def get_list(self):
        print >> sys.stderr, 'making get request to: %s%s' % (self.dest, self.path)

        data = {}

        if self.count:
            data.update({'count': self.count})

        if self.status:
            data.update({'status_filter':  '-'.join(map(lambda x: str(x), self.status))})

        data = urllib.urlencode(data)
        url = "%s/%s?%s" % (self.dest, self.path, data)

        request = urllib2.Request(url, headers=self.headers)
        BaseObject._execute(self, request)
