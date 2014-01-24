
from mainAPI import *

import json

# =======================================================
# USAGE
# =======================================================

def usage():
        print """
Synopsis:
    Uses Python API client to do some batch processing, in this 
    case bulk media transcribe. 

Usage:
    python transcribe_media.py [options]

Options
    -c, --count               Limit number of media to transcribe in this request
    -v, --verbose             Print out details about the process, handy for debugging
    -h, --help                Print this message ;-)

""";
        sys.exit()

# =======================================================
# MAIN
# =======================================================

def main(argv=None):

    if argv is None:
        argv = sys.argv

    verbose = False
    count = None

    opts, args = getopt.getopt(argv[1:], "vhc:", ["verbose", "help", "count="])

    for o, a in opts:
        if o in ("-h","--help"):
            usage()
        elif o in ("-v","--verbose"):
            # TODO: the goggles do nothing!
            verbose = True
        elif o in ("-c", "--count"):
            count = int(a)
        else:
            print 'Wrong option '+o+'\n'
            usage()

    # first get list of uploads
    register_openers()

    uid = None
    process_id = None
    accept='application/json'
    audioFilename = None
    metadataFilename = None
    transcriptFilename = None
    service = None
    item_id = None
    username='changeme'
    password='changeme'

    object_type = 'Media'
    action = 'get_list'
    status = [ STATUS_CODE['TRANSCODE'] ]

    inst = globals()[object_type](accept, username, password, uid, process_id,
                                  audioFilename, metadataFilename, transcriptFilename,
                                  service, item_id, count, status)
    try:
        func = getattr(inst, action)
        func()
    except urllib2.HTTPError, e:
        print >> sys.stderr, "error"
        print >> sys.stderr, e
        print >> sys.stderr, e.read()
        raise e

    media_list = json.loads(inst.response.read())

    for m in media_list['media'][:count]:
        if m['progress'] == 100:
            print m['clientfilename'], m['status']

            accept = 'text/xml'
            audioFilename=None
            metadataFilename=None
            uid = m['uuid']

            action = 'transcribe'
            inst = globals()[object_type](accept, username, password, uid, process_id, audioFilename, metadataFilename, transcriptFilename, service, item_id)
            try:
                func = getattr(inst, action)
                func()
            except urllib2.HTTPError, e:
                print >> sys.stderr,"error"
                print >> sys.stderr,e
                print >> sys.stderr,e.read()

if __name__=="__main__":
    main()

