#!/usr/bin/env python

from aptquery import do_query_APT_service
import getopt
import sys

def usage():
    print "Usage: apt_test_license_n_auth.py [-H HOST] [-p PORT]"

LICENSE_N_AUTH_TEXT = """
apt001    apt    Kxc23!fd#
apt_test_001    apt_test    5ks12%$
iTest_001    iTest    kcvO95L
svr_status_001    svr_status    &dBd231
tc001    tc    9kew#a$
tc001    tc_dd    e3&23djk
mr001    mr    iUd1512N
"""
#"invalide_license    xxx    xxx"
#"apt_test_001    apt_test    wrong_password"


def split_test_text(test_text):
    
    r = []
    for line in test_text.split('\n'):
        if len(line) == 0:
            continue
        r.append(line.split())
    return r

def main():
    host = "localhost"
    port = 80
    license_id = 'apt_test_001'
    username = 'apt_test'
    password = '5ks12%$'
    timeout = 1

    try:
        optlist, args = getopt.getopt(sys.argv[1:], 'H:p:h')
    except getopt.GetoptError as e:
        print e.msg
        return
    for k, v in optlist:
        if k == '-H':
            host = v
        elif k == '-p':
            port = int(v)
        elif k == '-h':
            usage()
            return 127

    query_parameters = { 
            'PROTOCOL_VER': '1',
            'LICENSE': license_id,
            'USER_NAME': username,
            'PASSWORD': password,
            'SERVICE_TYPE_ID': '1',
            'RESERVED': '',
            'DBG_FLAG': '0',
            'QUERY_PARAMETER': '1',
            'QUERY_VALUE': 'www.example.com'}
    r = split_test_text(LICENSE_N_AUTH_TEXT)
    exit_result = 0
    for record in r:
        query_parameters['LICENSE'] = record[0]
        query_parameters['USER_NAME'] = record[1]
        query_parameters['PASSWORD'] = record[2]
        result = do_query_APT_service(query_parameters, host=host, port=port, timeout=timeout, retry = 3)
        
        if result['HTTPCode'] == 0:
            print result
            print '[%3s]: %s, %s'%(result['HTTPCode'], str(record), result['ErrorMsg'])
            exit_result = 1
        elif result['HTTPCode'] != 200:
            print '[%3s]: %s, %s'%(result['HTTPCode'], str(record), result['DecryptedMessage'])
            exit_result = 1
        else:
            print '[%3s]: %s'%(result['HTTPCode'], str(record))

    return exit_result

if __name__ == '__main__':   
    sys.exit(main())
