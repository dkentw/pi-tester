#!/usr/bin/env python

import getopt
import sys

from aptquery import do_query_APT_service

def usage():
    print 'usage: aptcheck.py [-H host] [-p port] [-t time_out]'

def main():
    host = "localhost"
    port = 80
    license_id = 'svr_status_001'
    username = 'svr_status'
    password = '&dBd231'
    timeout = 2
    
    try:
        optlist, args = getopt.getopt(sys.argv[1:], 'H:p:t:h')
    except getopt.GetoptError as e:
        print e.msg
        return 0
    for k, v in optlist:
        if k == '-H':
            host = v
        elif k == '-p':
            port = int(v)
        elif k == '-t':
            timeout = int(v)
        elif k == '-h':
            usage()
            return
    if len(args) != 0:
        usage()
        return 127
    
    query_parameters = { 
            'PROTOCOL_VER': '1',
            'LICENSE': license_id,
            'USER_NAME': username,
            'PASSWORD': password,
            'SERVICE_TYPE_ID': '0',
            'RESERVED': '',
            'DBG_FLAG': '0',
            'QUERY_PARAMETER': '0',
            'QUERY_VALUE': ''}   
    result = do_query_APT_service(query_parameters, host=host, port=port, timeout=timeout, retry = 3)
    if result['HTTPCode'] == 0:
        # connectio failure or empty reply
        print 'SERVICE STATUS: offline'
        print 'Checked service %s:%s, ERROR=%s'%(host, port, result['ErrorMsg'] )
        return 2
    elif result['HTTPCode'] != 200:
        print 'SERVICE STATUS: partially down'
        print result['DecryptedMessage']
        return 1
    else:
        print 'SERVICE STATUS: OK'
        return 0


if __name__ == '__main__':   
    sys.exit(main())
