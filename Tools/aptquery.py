#!/usr/bin/env python

import sys
import os
import pprint
import traceback
try:
    import simplejson as json
except ImportError: # pragma: no cover
    import json

import getopt
import pycurl
import StringIO


sys.path.append(os.path.join(os.path.dirname(__file__), '..')) # for module "apt" 

# Ignore signale pipe for socket operations.
try:
    import signal
    from signal import SIGPIPE, SIG_IGN
    signal.signal(signal.SIGPIPE, signal.SIG_IGN)
except ImportError:
    pass 

from aptlib.crypto import APTCipher

from collections import deque

class AsyncHTTPClient:
    def __init__(self, 
                 max_connection=20, 
                 timeout = 2, 
                 retry = 3,
                 follow_location = False,
                 max_redirs = 3,
                 connect_timeout = 3,
                 ):
        self.max_connection = max_connection
        self.mc = pycurl.CurlMulti()
        # OPTIONS
        self.timeout = timeout
        self.retry = retry
        self.follow_location = follow_location
        self.max_redirs =max_redirs
        self.connect_timeout = connect_timeout
        
        self.req_queue = deque()
        self.all_curl = deque()  # for weak ref
        self.free_curl = deque() 
        for _ in xrange(max_connection):
            c = pycurl.Curl()
            c.setopt(pycurl.PROXY, "")
            c.setopt(pycurl.FOLLOWLOCATION, self.follow_location)
            c.setopt(pycurl.MAXREDIRS, self.max_redirs)
            c.setopt(pycurl.CONNECTTIMEOUT, self.connect_timeout)
            c.setopt(pycurl.TIMEOUT, self.timeout)
            c.setopt(pycurl.NOSIGNAL, 1)
            self.free_curl.append(c)
            self.all_curl.append(c)
        
        pass
    def __len__(self):
        return len(self.req_queue) + self.max_connection - len(self.free_curl)
    
    def close(self):
        pass
    
    def queue_request(self, url, context, **kwargs):
        self.req_queue.append((url, context, kwargs))
    
    def _reuse_curl(self, c, req, retry = 0):
        c.setopt(pycurl.URL, req[0])
        c.context = req[1]
        c.req = req
        b = StringIO.StringIO() # response body 
        h = StringIO.StringIO() # response header
        c.setopt(pycurl.WRITEFUNCTION, b.write)
        c.setopt(pycurl.HEADERFUNCTION, h.write)
        c.body_wr = b
        c.header_wr = h
        c.retry = retry

    # @return list of result. RESULT => (context, retry_times, HTTP_CODE, HEADER/ERRNO, CONTENT/ERR_MESSAGE)
    # HTTP_CODE <0 connection error.
    def perform(self, select_interval=0.1):
        # if simulanneous connection < max_sim, and there are requests in queue.
        while self.free_curl and self.req_queue:
            curl = self.free_curl.pop()
            req = self.req_queue.popleft()
            self._reuse_curl(curl, req)
            self.mc.add_handle(curl)

        num_handles = 1
        if self.mc.select(select_interval) < 0:
            return []                
        while 1:
            ret, num_handles = self.mc.perform()
            if ret != pycurl.E_CALL_MULTI_PERFORM:
                break                        
            
        req_done = []   
        num_q, ok_list, err_list = self.mc.info_read()
        
        for c in ok_list:
            #print "Success:", c.url, c.getinfo(pycurl.EFFECTIVE_URL)
            self.free_curl.append(c)
            req_done.append((c.context, c.retry, c.getinfo(pycurl.HTTP_CODE), c.header_wr.getvalue(), c.body_wr.getvalue()))
            self.mc.remove_handle(c)
            
        for c, errno, errmsg in err_list:
            #print "FAIL: ", c.getinfo(pycurl.EFFECTIVE_URL)
            self.mc.remove_handle(c)
            if c.retry < self.retry:
                self._reuse_curl(c, c.req, c.retry+1)
                self.mc.add_handle(c)
            else:
                self.free_curl.append(c)
                req_done.append((c.context, c.retry, 0, errno, errmsg))

        return req_done        
     
    
        


class APTQuery:
    def __init__(self, license, username, password, dbgflag = False, host = 'localhost', port = 80, timeout = 3, retry = 3):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.retry = retry
        
        self.protocol_ver = '1' 
        self.license = license
        self.username = username
        self.password = password
        self.reserve = ''
        if dbgflag == True:
            self.dbg_flag = '1'
        else:
            self.dbg_flag = '0'
        self.async_cli = AsyncHTTPClient(50, timeout=timeout, retry=retry)
    def __len__(self):
        return len(self.async_cli)
    
    def queue_query(self, service_ID, q_param, q_v, context = None):
        args_str = '/'.join([self.protocol_ver, self.license, self.username, self.password, service_ID, self.reserve, self.dbg_flag, q_param, q_v])
        result = {}
        cipher = APTCipher('0')
        encrypted_args_str = cipher.encrypt(args_str)
        
        url = "http://%s:%d/U0/%d/%s"%(self.host, self.port, len(encrypted_args_str), encrypted_args_str)
        result['RawParameter'] = args_str
        result['HTTPRequest'] = url
        result['Context'] = context
        
        self.async_cli.queue_request(url, result)
    def perform(self):
        http_result_list = self.async_cli.perform()
        if len(http_result_list) == 0:
            return []
        result_list = []
        for http_result in http_result_list: #(context, retry_times, HTTP_CODE, HEADER, CONTENT)
            #decrypted_msg = '[]'
            result = http_result[0]
            http_code = http_result[2]
            encrypted_msg = http_result[4]
            header = http_result[3]
            #if c.getinfo(pycurl.HTTP_CODE) == 200:
            try:
                decrypted_msg = ''
                size, crypted_msg = encrypted_msg.split('/', 1)
                if len(crypted_msg) != int(size):
                    raise 'size not match, size(%s), msg="%s"'%(size, crypted_msg)
                cipher = APTCipher('0')
                decrypted_msg = cipher.decrypt(crypted_msg)
                decrypted_msg = decrypted_msg
            except BaseException as e:
                decrypted_msg = 'unable decrypt msg "%s", %s'%(decrypted_msg, str(e))
            result['HTTPCode'] = http_code
            result['HTTPHeader'] = header
            result['HTTPResponse'] = encrypted_msg
            result['DecryptedMessage'] = decrypted_msg
            result['Retry'] = http_result[1]
            result_list.append(result)
        return result_list

    def query(self, service_ID, q_param, q_v):        
        args_str = '/'.join([self.protocol_ver, self.license, self.username, self.password, service_ID, self.reserve, self.dbg_flag, q_param, q_v])
        result = {}
        result['RawParameter'] = args_str
        cipher = APTCipher('0')
        
        encrypted_args_str = cipher.encrypt(args_str)
        
        url = "http://%s:%d/U0/%d/%s"%(host, port, len(encrypted_args_str), encrypted_args_str)
        result['HTTPRequest'] = url
        
        #c.setopt(pycurl.FOLLOWLOCATION, 1) # redirect
        for _ in xrange(retry): # max N times
            c = pycurl.Curl()
            b = StringIO.StringIO() # response body 
            h = StringIO.StringIO() # response header
            try:
                c.setopt(pycurl.URL, url)
                c.setopt(pycurl.PROXY, "") # disable proxy
                c.setopt(pycurl.WRITEFUNCTION, b.write)
                c.setopt(pycurl.HEADERFUNCTION, h.write)
                c.setopt(pycurl.TIMEOUT, timeout)
                c.perform()
                break
            except pycurl.error as e:
                #print 'retrying...........'
                #traceback.print_exc()
                result['ErrorMsg'] = str(e)
                continue
        else:
            result['HTTPCode'] = 0
            result['HTTPHeader'] = ''
            result['HTTPResponse'] = ''
            result['DecryptedMessage'] = ''
            return result
            
        #decrypted_msg = '[]'
        encrypted_msg = b.getvalue()
        #if c.getinfo(pycurl.HTTP_CODE) == 200:
        try:
            decrypted_msg = ''
            size, crypted_msg = encrypted_msg.split('/', 1)
            if len(crypted_msg) != int(size):
                raise 'size not match, size(%s), msg="%s"'%(size, crypted_msg)
            cipher = APTCipher('0')
            decrypted_msg = cipher.decrypt(crypted_msg)
            decrypted_msg = decrypted_msg
        except BaseException as e:
            decrypted_msg = 'unable decrypt msg "%s", %s'%(decrypted_msg, str(e))
        result['HTTPCode'] = c.getinfo(pycurl.HTTP_CODE)
        result['HTTPHeader'] = h.getvalue()
        result['HTTPResponse'] = encrypted_msg
        result['DecryptedMessage'] = decrypted_msg
        return result        


def do_query_APT_service(query_parameters, host = 'localhost', port = 80, timeout = 3, retry = 3):
    args = [
            query_parameters['PROTOCOL_VER'],
            query_parameters['LICENSE'],
            query_parameters['USER_NAME'],
            query_parameters['PASSWORD'],
            query_parameters['SERVICE_TYPE_ID'],
            query_parameters['RESERVED'],
            query_parameters['DBG_FLAG'],
            query_parameters['QUERY_PARAMETER'],
            query_parameters['QUERY_VALUE'] ]
    args_str = '/'.join(args)
    result = {}
    result['RawParameter'] = args_str
    cipher = APTCipher('0')
    
    encrypted_args_str = cipher.encrypt(args_str)
    
    url = "http://%s:%d/U0/%d/%s"%(host, port, len(encrypted_args_str), encrypted_args_str)
    result['HTTPRequest'] = url
    
    #c.setopt(pycurl.FOLLOWLOCATION, 1) # redirect
    for _ in xrange(retry): # max 3 times
        c = pycurl.Curl()
        b = StringIO.StringIO() # response body 
        h = StringIO.StringIO() # response header
        try:
            c.setopt(pycurl.URL, url)
            c.setopt(pycurl.PROXY, "") 
            c.setopt(pycurl.WRITEFUNCTION, b.write)
            c.setopt(pycurl.HEADERFUNCTION, h.write)
            c.setopt(pycurl.TIMEOUT, timeout)
            c.perform()
            break
        except pycurl.error as e:
            #print 'retrying...........'
            #traceback.print_exc()
            result['ErrorMsg'] = str(e)
            continue
    else:
        result['HTTPCode'] = 0
        result['HTTPHeader'] = ''
        result['HTTPResponse'] = ''
        result['DecryptedMessage'] = ''
        return result
        
    #decrypted_msg = '[]'
    encrypted_msg = b.getvalue()
    #if c.getinfo(pycurl.HTTP_CODE) == 200:
    try:
        decrypted_msg = ''
        size, crypted_msg = encrypted_msg.split('/', 1)
        if len(crypted_msg) != int(size):
            raise 'size not match, size(%s), msg="%s"'%(size, crypted_msg)
        cipher = APTCipher('0')
        decrypted_msg = cipher.decrypt(crypted_msg)
        decrypted_msg = decrypted_msg
    except BaseException as e:
        decrypted_msg = 'unable decrypt msg "%s", %s'%(decrypted_msg, str(e))
    result['HTTPCode'] = c.getinfo(pycurl.HTTP_CODE)
    result['HTTPHeader'] = h.getvalue()
    result['HTTPResponse'] = encrypted_msg
    result['DecryptedMessage'] = decrypted_msg
    return result

def validate_query_parameters(query_parameters):
    args = [
            query_parameters['PROTOCOL_VER'],
            query_parameters['LICENSE'],
            query_parameters['USER_NAME'],
            query_parameters['PASSWORD'],
            query_parameters['SERVICE_TYPE_ID'],
            query_parameters['RESERVED'],
            query_parameters['DBG_FLAG'],
            query_parameters['QUERY_PARAMETER'],
            query_parameters['QUERY_VALUE'] ]
    args_str = '/'.join(args)
    #import views
    from info.request_processor import RequestProcessor
    req = RequestProcessor(args_str)
    req.validate_args()

def main():
    host = "localhost"
    port = 80
    license_id = 'apt_test_001'
    username = 'apt_test'
    password = '5ks12%$'
    try:
        optlist, args = getopt.getopt(sys.argv[1:], 'U:P:l:H:p:h')
    except getopt.GetoptError as e:
        print e.msg
        return
    for k, v in optlist:
        if k == '-H':
            host = v
        elif k == '-p':
            port = int(v)
        elif k == '-l':
            license_id = v
        elif k == '-U':
            username = v
        elif k == '-P':
            password = v
        elif k == '-h':
            usage()
            return
    if len(args) != 3:
        usage()
        return
        
    query_parameters = { 
            'PROTOCOL_VER': '1',
            'LICENSE': license_id,
            'USER_NAME': username,
            'PASSWORD': password,
            'SERVICE_TYPE_ID': args[0],
            'RESERVED': '',
            'DBG_FLAG': '1',
            'QUERY_PARAMETER': args[1],
            'QUERY_VALUE': args[2]}    

    #validate_query_parameters(query_parameters)
    result = do_query_APT_service(query_parameters, host, port)
    print """== Request =============================
PROTOCOL_VER: %(PROTOCOL_VER)s
LICENSE: %(LICENSE)s
USER_NAME: %(USER_NAME)s
PASSWORD: %(PASSWORD)s
SERVICE_TYPE_ID: %(SERVICE_TYPE_ID)s
RESERVED: %(RESERVED)s
DBG_FLAG: %(DBG_FLAG)s
QUERY_PARAMETER: %(QUERY_PARAMETER)s
QUERY_VALUE: %(QUERY_VALUE)s"""%(query_parameters)
    print"""
RawParameter: %(RawParameter)s
HTTPRequest: %(HTTPRequest)s

== Response ============================
HTTPCode: %(HTTPCode)s
HTTPHeader: %(HTTPHeader)s
HTTPResponse:\n%(HTTPResponse)s\n
DecryptedMessage:\n%(DecryptedMessage)s
"""%(result)
    if result['HTTPCode'] == 0:
        print 'SERVICE STATUS: offline'
        print 'Checked service %s:%s, ERROR=%s'%(host, port, result['ErrorMsg'] )
        
def usage():
    print """
Usage: aptquery.py [-H HOST] [-p PORT] [-l license] [-U username] [-P password] SERVICE_TYPE_ID QUERY_PARAMETER QUERY_VALUE
Test query APT service with encrypted protocol.

Example:
  # for C&C search
  aptquery.py -H 127.0.0.1 -p 8000 1 1 2.229.10.5
  # for file SHA1 search
  aptquery.py -H 127.0.0.1 -p 8000 4 0 bb36c0d0d56510551e17d4e161ba436f0034c1bc
  # for C&C extensive view
  aptquery.py -H 127.0.0.1 -p 8000 7 0 747cdce85ddbf8c45dc014c06efcc122afaa7d6e
  # for file extensive view
  aptquery.py -H 127.0.0.1 -p 8000 8 0 bb36c0d0d56510551e17d4e161ba436f0034c1bc
  
  # find no result
  aptquery.py -H 127.0.0.1 -p 8000 1 1 www.xxx.com
  # have result on SHA1, but no result on extensive view
  aptquery.py -H 127.0.0.1 -p 8000 4 0 44306a93578229c8b1f461ca3ca6d5ef3cdc1755
  aptquery.py -H 127.0.0.1 -p 8000 8 0 44306a93578229c8b1f461ca3ca6d5ef3cdc1755
  
  

SERVICE_TYPE_ID
1) Search by IP/domain/URL (exactly match)
4) Search by file SHA1
5) Get APT Info by APT Info Node UID
7) Get CnC Extensive View by Node UID
8) Get File Extensive View by Node UID
Ref=> http://coretech-backend-dev.tw.trendnet.org/wiki/APT_Info_Service_Request_SPEC#Summary
"""

if __name__ == '__main__':
    main()
