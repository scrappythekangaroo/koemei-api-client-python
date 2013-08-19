import sys, urllib2, urllib, os
from encode import multipart_encode, MultipartParam


def read_file(filename):
    fp = open(os.path.abspath(filename), "r")
    file_content = fp.read()
    fp.close()

    return file_content


from BaseObject import BaseObject


class Media(BaseObject):
    def __init__(self, accept, username="", password="", uid="", process_id="", audioFilename=None,
                 metadataFilename=None, transcriptFilename=None,
                 service=None, item_id=None, count=None, status=None):
        BaseObject.__init__(self, accept, username=username, password=password, uid=uid, process_id=process_id,
                            audioFilename=audioFilename, metadataFilename=metadataFilename, transcriptFilename=transcriptFilename,
                            service=service, item_id=item_id, count=count, status=status)
        self.path = 'media/'
        self.path_trans = '/transcribe'
        self.path_publish = '/publish'
        self.path_unpublish = '/unpublish'

    @BaseObject._reset_headers
    def get(self):
        print >> sys.stderr, 'making get request to: %s%s' % (self.dest, self.path + self.uid)
        request = urllib2.Request(self.dest + self.path + self.uid, headers=self.headers)
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

    @BaseObject._reset_headers
    def create(self):
        print >> sys.stderr, 'making post request to: %s%s' % (self.dest, self.path)

        data = {}
        if self.service:
            data.update({'service': self.service,
                         'item_id': self.item_id})

        if 'http' in self.audioFilename:
            data.update({'media': self.audioFilename})
        else:
            data.update({'media': open(self.audioFilename, "rb")})

        if self.transcriptFilename:
            self.datagen.update({'transcript': read_file(self.transcriptFilename)})

        headers = self.headers
        data, headers_ = multipart_encode(data)
        headers.update(headers_)

        request = urllib2.Request(self.dest + self.path, data=data, headers=headers)

        BaseObject._execute(self, request)

    @BaseObject._reset_headers
    def transcribe(self, success_callback_url='', error_callback_url=''):
        print >> sys.stderr, 'making post request to: %s%s' % (self.dest, self.path + self.uid + self.path_trans)

        data = urllib.urlencode(
            {'success_callback_url': success_callback_url, 'error_callback_url': error_callback_url, })
        request = urllib2.Request(self.dest + self.path + self.uid + self.path_trans, data=data, headers=self.headers)
        BaseObject._execute(self, request)


    @BaseObject._reset_headers
    def publish(self):
        print >> sys.stderr, 'making put request to: %s%s' % (self.dest, self.path + self.uid + self.path_publish)

        data = {}
        if self.service:
            data.update({'service_name': self.service,})

        data = urllib.urlencode(data)
        url = "%s/%s/%s/%s?%s" % (self.dest, self.path, self.uid, self.path_publish, data)

        request = urllib2.Request(url, data="", headers=self.headers)
        request.get_method = lambda: 'PUT'
        BaseObject._execute(self, request)

    @BaseObject._reset_headers
    def unpublish(self):
        print >> sys.stderr, 'making put request to: %s%s' % (self.dest, self.path + self.uid + self.path_unpublish)
        request = urllib2.Request(self.dest + self.path + self.uid + self.path_unpublish, data="", headers=self.headers)
        request.get_method = lambda: 'PUT'
        BaseObject._execute(self, request)
