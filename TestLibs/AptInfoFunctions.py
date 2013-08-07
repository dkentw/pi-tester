'''
Created on 2012/6/21

@author: Kent

Here place the libraries for testing APT Info Service
'''
import httplib
import pycurl
import base64
import binascii
import StringIO
import logging

from Crypto.Cipher import AES
_CS_CIPHER_AES_BLOCK_SIZE   = 16
_CS_CIPHER_AES_MODE         = AES.MODE_CBC
_CS_CIPHER_AES_PADDING      = '\0'
_CS_CIPHER_T_B64_ALTCHARS   = '-_'

TMUFE_CIPHER_MAP = {
    '0': (binascii.a2b_hex('2401cc56317a30437812b73a77213352'), binascii.a2b_hex('ab120c55612a30c3c81bb2317d2f3a01')),
    '1': (binascii.a2b_hex('b7f902d3ca23176832c2f82305612970'), binascii.a2b_hex('39df0c25752f64241237789a80431bcc')),
}
    
def HTTPRequest(url, port, message):
    '''
    response.getheaders(): show headers
    response.status: show status code
    response.reason: show reason
    '''
    connection = httplib.HTTPConnection(url)
    connection.request('GET', message)
    response = connection.getresponse()
    connection.close()
    return response
    
def APTQuery(testParameter):
    args = [testParameter['PROTOCOL_VER'], testParameter['LICESE_ID'], testParameter['USERNAME'],
            testParameter['PASSWORD'], testParameter['SERVICE_TYPE'], testParameter['RESERVED'],
            testParameter['DBG_FLAG'], testParameter['QUERY_PARAMETER'], testParameter['QUERY_VALUE']]   
    args_str = '/'.join(args)
   
    # encrypted message   
    encrypted_msg = AESEncrypt(args_str)
    
    # send request
    url = "http://%s:%d/U0/%d/%s"%(testParameter['TEST_HOST'], testParameter['TEST_PORT'], len(encrypted_msg), encrypted_msg)
    encrypted_response = cURL(url)
    
    # Decrypt response
    decrypted_res = AESDecrypt(encrypted_response)
    
        
    return decrypted_res
    # ...
    
def AESEncrypt(msg):
    cipher = GetCipher(TMUFE_CIPHER_MAP['0'])
    s = len(msg) % _CS_CIPHER_AES_BLOCK_SIZE
    if s != 0:
        msg = msg + (_CS_CIPHER_AES_BLOCK_SIZE - s) * _CS_CIPHER_AES_PADDING    
    return base64.b64encode(cipher.encrypt(msg), altchars = _CS_CIPHER_T_B64_ALTCHARS)

def AESDecrypt(encrypted_msg):
    try:
        size, crypted_msg = encrypted_msg.split('/', 1)
        if len(crypted_msg) != int(size):
            raise 'size not match, size(%s), msg="%s"'%(size, crypted_msg)
        cipher = GetCipher(TMUFE_CIPHER_MAP['0'])
    except BaseException as error:
        logging.error('There are some error: {0}'.format(*str(error)))
        
    try:
        decrypted_msg = cipher.decrypt(base64.b64decode(crypted_msg, altchars = _CS_CIPHER_T_B64_ALTCHARS)).rstrip(_CS_CIPHER_AES_PADDING)
    except BaseException as e:
        print 'unable decrypt msg "%s", %s'%(encrypted_msg, str(e))
        
    return decrypted_msg

def GetCipher(TMUFE_CIPHER):
    key, iv = TMUFE_CIPHER
    return AES.new(key , _CS_CIPHER_AES_MODE, iv)
            
def cURL(url):
    c = pycurl.Curl()
    body = StringIO.StringIO() # response body 
    header = StringIO.StringIO() # response header
    try:
        timeout = 3
        c.setopt(pycurl.URL, url)
        c.setopt(pycurl.PROXY, "") 
        c.setopt(pycurl.WRITEFUNCTION, body.write)
        c.setopt(pycurl.HEADERFUNCTION, header.write)
        c.setopt(pycurl.TIMEOUT, timeout)
        c.perform()
    except pycurl.error as e:
        print e
        
    return body.getvalue()
    
    
    
        
        