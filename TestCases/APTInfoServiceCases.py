'''
Created on 2012/6/21
@author: kent

Here create your test cases.

<Format>
class TestCaseID:
    def __init__(self):
        <initial data>
        
    def run(self):
        <test steps>
'''
import re
import logging
import TestLibs.AptInfoFunctions as TestLib

testParameter = {
                 'TEST_HOST': "10.1.168.63",
                 'TEST_PORT': 80,
                 'PROTOCOL_VER': '1',
                 'LICESE_ID' : 'apt_test_001',
                 'USERNAME' : 'apt_test',
                 'PASSWORD' : '5ks12%$',
                 'SERVICE_TYPE' : '0',
                 'RESERVED' : '',
                 'DBG_FLAG' : '0',  
                 'QUERY_PARAMETER' : '0',
                 'QUERY_VALUE' : 'www.yahoo.com.tw' 
}

class HTTPConnectToYahoo:
    '''
    Check the connection to Yahoo
    '''
    def __init__(self):
        self.url = 'tw.yahoo.com'
        self.port = '80'
        self.message = ''
        
    def run(self):
        result = TestLib.HTTPRequest(self.url, self.port, self.message)
        if result.status == 200:
            return True
        else:
            print result.status
            print result.reason
            return False
    
class HTTPConnectToGoogle:
    '''
    Check the connection to Google   
    '''
    def __init__(self):
        self.url = 'www.google.com.tw'
        self.port = '80'
        self.message = ''
        
    def run(self):
        result = TestLib.HTTPRequest(self.url, self.port, self.message)
        return True if result.status == 200 else False
    
class APT0101:
    def __init__(self):
        self.url = testParameter['TEST_HOST']
        self.port = ''
        self.message = ''    
 
    def run(self):
        try:
            result = TestLib.HTTPRequest(self.url, self.port, self.message)
        except:
            logging.error("status: {0}, reason: {1}".format(result.status, result.reason))
        logging.info("status: {0}, reason: {1}".format(result.status, result.reason))
        return True if result.status == 200 else False

class APT0102:
    def __init__(self):
        self.url = testParameter['TEST_HOST']
        self.port = ''
        self.message = 'foo'
        
    def run(self):
        result = TestLib.HTTPRequest(self.url, self.port, self.message)
        logging.info("status: {0}, reason: {1}".format(result.status, result.reason))
        return True if result.status != 200 else False

class APT0103:
    def __init__(self):
        self.testParameter = {
                 'TEST_HOST': "10.1.168.63",
                 'TEST_PORT': 80,
                 'PROTOCOL_VER': '1',
                 'LICESE_ID' : 'apt_test_001',
                 'USERNAME' : 'apt_test',
                 'PASSWORD' : '5ks12%$',
                 'SERVICE_TYPE' : '1',
                 'RESERVED' : '',
                 'DBG_FLAG' : '1',  
                 'QUERY_PARAMETER' : '1',
                 'QUERY_VALUE' : '203.70.58.177' 
        }
        self.pattern = r'{"dbg_info": {"user_cache_info": "positive hit", "cache_info": "hit"}, "uid_list": [{"_id": "74d402341693f912e8606952b52f12adf8dfdd93"}]}'
    def run(self):
        try:
            result = TestLib.APTQuery(self.testParameter)
            #logging.info(result)
        except:
            result = False
        return True if result == self.pattern else False

class APT0104:
    def __init__(self):
        self.testParameter = {
                 'TEST_HOST': "10.1.168.63",
                 'TEST_PORT': 80,
                 'PROTOCOL_VER': '1',
                 'LICESE_ID' : 'apt_test_001',
                 'USERNAME' : 'apt_test',
                 'PASSWORD' : '5ks12%$',
                 'SERVICE_TYPE' : '1',
                 'RESERVED' : '',
                 'DBG_FLAG' : '1',  
                 'QUERY_PARAMETER' : '1',
                 'QUERY_VALUE' : 'root.rootbitch.com' 
        }
        self.pattern = r'{"dbg_info": {"user_cache_info": "positive hit", "cache_info": "hit"}, "uid_list": [{"_id": "621c7466d2728b91375d8b06965a39e77e03a06f"}]}'
    def run(self):
        try:
            result = TestLib.APTQuery(self.testParameter)
        except:
            result = False
        logging.info(result)
        return True if result == self.pattern else False

class APT0105:
    def __init__(self):
        self.testParameter = {
                 'TEST_HOST': "10.1.168.63",
                 'TEST_PORT': 80,
                 'PROTOCOL_VER': '1',
                 'LICESE_ID' : 'apt_test_001',
                 'USERNAME' : 'apt_test',
                 'PASSWORD' : '5ks12%$',
                 'SERVICE_TYPE' : '1',
                 'RESERVED' : '',
                 'DBG_FLAG' : '1',  
                 'QUERY_PARAMETER' : '1',
                 'QUERY_VALUE' : 'http%3A//203.70.58.177%3A1998782544/AWS25804.jsp%3FbZTn8sLn8gl9jOmKjO9mI/HwjndMIOmmjkHK' 
        }
        self.pattern = r'{"dbg_info": {"user_cache_info": "positive hit", "cache_info": "hit"}, "uid_list": [{"_id": "f89a2997e8742b051cda853110bfb0c228b6ab36"}]}'
    def run(self):
        result = TestLib.APTQuery(self.testParameter)
        logging.info(result)
        return True if result == self.pattern else False

class APT0106:
    def __init__(self):
        self.testParameter = {
                 'TEST_HOST': "10.1.168.63",
                 'TEST_PORT': 80,
                 'PROTOCOL_VER': '1',
                 'LICESE_ID' : 'apt_test_001',
                 'USERNAME' : 'apt_test',
                 'PASSWORD' : '5ks12%$',
                 'SERVICE_TYPE' : '4',
                 'RESERVED' : '',
                 'DBG_FLAG' : '1',  
                 'QUERY_PARAMETER' : '0',
                 'QUERY_VALUE' : 'ff536b7a2e791d9fb7fa0567d29e99d59cc3f1e8' 
        }
        self.pattern = r'{"dbg_info": {"user_cache_info": "positive hit", "cache_info": "hit"}, "uid_list": [{"_id": "ff536b7a2e791d9fb7fa0567d29e99d59cc3f1e8"}]}'
    def run(self):
        result = TestLib.APTQuery(self.testParameter)
        logging.info(result)
        return True if result == self.pattern else False

class APT0107:
    def __init__(self):
        self.testParameter = {
                 'TEST_HOST': "10.1.168.63",
                 'TEST_PORT': 80,
                 'PROTOCOL_VER': '1',
                 'LICESE_ID' : 'apt_test_001',
                 'USERNAME' : 'apt_test',
                 'PASSWORD' : '5ks12%$',
                 'SERVICE_TYPE' : '1',
                 'RESERVED' : '',
                 'DBG_FLAG' : '1',  
                 'QUERY_PARAMETER' : '1',
                 'QUERY_VALUE' : '203.70.58.177' 
        }
        self.pattern = r'{"dbg_info": {"user_cache_info": "positive hit", "cache_info": "hit"}, "uid_list": [{"_id": "74d402341693f912e8606952b52f12adf8dfdd93"}]}'
    def run(self):
        result = TestLib.APTQuery(self.testParameter)
        logging.info(result)
        return True if result == self.pattern else False

class APT0108:
    def __init__(self):
        self.testParameter = {
                 'TEST_HOST': "10.1.168.63",
                 'TEST_PORT': 80,
                 'PROTOCOL_VER': '1',
                 'LICESE_ID' : 'apt_test_001',
                 'USERNAME' : 'apt_test',
                 'PASSWORD' : '5ks12%$',
                 'SERVICE_TYPE' : '1',
                 'RESERVED' : '',
                 'DBG_FLAG' : '1',  
                 'QUERY_PARAMETER' : '1',
                 'QUERY_VALUE' : '203.70.58.177' 
        }
        self.pattern = r'{"dbg_info": {"user_cache_info": "positive hit", "cache_info": "hit"}, "uid_list": [{"_id": "74d402341693f912e8606952b52f12adf8dfdd93"}]}'
    def run(self):
        result = TestLib.APTQuery(self.testParameter)
        logging.info(result)
        return True if result == self.pattern else False

class APT0109:
    def __init__(self):
        self.testParameter = {
                 'TEST_HOST': "10.1.168.63",
                 'TEST_PORT': 80,
                 'PROTOCOL_VER': '1',
                 'LICESE_ID' : 'apt_test_001',
                 'USERNAME' : 'apt_test',
                 'PASSWORD' : '5ks12%$',
                 'SERVICE_TYPE' : '1',
                 'RESERVED' : '',
                 'DBG_FLAG' : '1',  
                 'QUERY_PARAMETER' : '1',
                 'QUERY_VALUE' : '203.70.58.177' 
        }
        self.pattern = r'{"dbg_info": {"user_cache_info": "positive hit", "cache_info": "hit"}, "uid_list": [{"_id": "74d402341693f912e8606952b52f12adf8dfdd93"}]}'
    def run(self):
        '''
        result = TestLib.APTQuery(self.testParameter)
        logging.info(result)
        return True if result == self.pattern else False
        '''
        return True

class APT0110:
    def __init__(self):
        self.testParameter = {
                 'TEST_HOST': "10.1.168.63",
                 'TEST_PORT': 80,
                 'PROTOCOL_VER': '1',
                 'LICESE_ID' : 'apt_test_001',
                 'USERNAME' : 'apt_test',
                 'PASSWORD' : '5ks12%$',
                 'SERVICE_TYPE' : '1',
                 'RESERVED' : '',
                 'DBG_FLAG' : '1',  
                 'QUERY_PARAMETER' : '1',
                 'QUERY_VALUE' : '203.70.58.177' 
        }
        self.pattern = r'{"dbg_info": {"user_cache_info": "positive hit", "cache_info": "hit"}, "uid_list": [{"_id": "74d402341693f912e8606952b52f12adf8dfdd93"}]}'
    def run(self):
        '''
        result = TestLib.APTQuery(self.testParameter)
        logging.info(result)
        return True if result == self.pattern else False
        '''
        return True
    
class APT0111:
    def __init__(self):
        self.testParameter = {
                 'TEST_HOST': "10.1.168.63",
                 'TEST_PORT': 80,
                 'PROTOCOL_VER': '1',
                 'LICESE_ID' : 'apt_test_001',
                 'USERNAME' : 'apt_test',
                 'PASSWORD' : '5ks12%$',
                 'SERVICE_TYPE' : '5',
                 'RESERVED' : '',
                 'DBG_FLAG' : '1',  
                 'QUERY_PARAMETER' : '1',
                 'QUERY_VALUE' : 'ff536b7a2e791d9fb7fa0567d29e99d59cc3f1e8' 
        }
        self.pattern = r'{"dbg_info": {"user_cache_info": "positive hit", "cache_info": "hit"}, "uid_list": [{"_id": "74d402341693f912e8606952b52f12adf8dfdd93"}]}'
    def run(self):
        result = TestLib.APTQuery(self.testParameter)
        logging.info(result)
        return True if result == self.pattern else False

class APT0112:
    def __init__(self):
        self.testParameter = {
                 'TEST_HOST': "10.1.168.63",
                 'TEST_PORT': 80,
                 'PROTOCOL_VER': '1',
                 'LICESE_ID' : 'apt_test_001',
                 'USERNAME' : 'apt_test',
                 'PASSWORD' : '5ks12%$',
                 'SERVICE_TYPE' : '1',
                 'RESERVED' : '',
                 'DBG_FLAG' : '1',  
                 'QUERY_PARAMETER' : '1',
                 'QUERY_VALUE' : '203.70.58.177' 
        }
        self.pattern = r'{"dbg_info": {"user_cache_info": "positive hit", "cache_info": "hit"}, "uid_list": [{"_id": "74d402341693f912e8606952b52f12adf8dfdd93"}]}'
    def run(self):
        result = TestLib.APTQuery(self.testParameter)
        logging.info(result)
        return True if result == self.pattern else False

class APT0113:
    def __init__(self):
        self.testParameter = {
                 'TEST_HOST': "10.1.168.63",
                 'TEST_PORT': 80,
                 'PROTOCOL_VER': '1',
                 'LICESE_ID' : 'apt_test_001',
                 'USERNAME' : 'apt_test',
                 'PASSWORD' : '5ks12%$',
                 'SERVICE_TYPE' : '1',
                 'RESERVED' : '',
                 'DBG_FLAG' : '1',  
                 'QUERY_PARAMETER' : '1',
                 'QUERY_VALUE' : '203.70.58.177' 
        }
        self.pattern = r'{"dbg_info": {"user_cache_info": "positive hit", "cache_info": "hit"}, "uid_list": [{"_id": "74d402341693f912e8606952b52f12adf8dfdd93"}]}'
    def run(self):
        result = TestLib.APTQuery(self.testParameter)
        logging.info(result)
        return True if result == self.pattern else False

class APT0114:
    def __init__(self):
        self.testParameter = {
                 'TEST_HOST': "10.1.168.63",
                 'TEST_PORT': 80,
                 'PROTOCOL_VER': '1',
                 'LICESE_ID' : 'apt_test_001',
                 'USERNAME' : 'apt_test',
                 'PASSWORD' : '5ks12%$',
                 'SERVICE_TYPE' : '1',
                 'RESERVED' : '',
                 'DBG_FLAG' : '1',  
                 'QUERY_PARAMETER' : '1',
                 'QUERY_VALUE' : '203.70.58.177' 
        }
        self.pattern = r'{"dbg_info": {"user_cache_info": "positive hit", "cache_info": "hit"}, "uid_list": [{"_id": "74d402341693f912e8606952b52f12adf8dfdd93"}]}'
    def run(self):
        result = TestLib.APTQuery(self.testParameter)
        logging.info(result)
        return True if result == self.pattern else False

class APT0201:
    def __init__(self):
        self.testParameter = {
                 'TEST_HOST': "10.1.168.63",
                 'TEST_PORT': 80,
                 'PROTOCOL_VER': '1',
                 'LICESE_ID' : 'apt_test_001xxxx',
                 'USERNAME' : 'apt_test',
                 'PASSWORD' : '5ks12%$',
                 'SERVICE_TYPE' : '1',
                 'RESERVED' : '',
                 'DBG_FLAG' : '1',  
                 'QUERY_PARAMETER' : '1',
                 'QUERY_VALUE' : '203.70.58.177' 
        }
        self.pattern = r'{"dbg_info": {}, "error_msg": "Invalid user license."}'
    def run(self):
        result = TestLib.APTQuery(self.testParameter)
        logging.info(result)
        return True if result == self.pattern else False
    
class APT0202:
    def __init__(self):
        self.testParameter = {
                 'TEST_HOST': "10.1.168.63",
                 'TEST_PORT': 80,
                 'PROTOCOL_VER': '1',
                 'LICESE_ID' : 'apt_test_001',
                 'USERNAME' : 'apt_testxxxx',
                 'PASSWORD' : '5ks12%$',
                 'SERVICE_TYPE' : '1',
                 'RESERVED' : '',
                 'DBG_FLAG' : '1',  
                 'QUERY_PARAMETER' : '1',
                 'QUERY_VALUE' : '203.70.58.177' 
        }
        self.pattern = re.compile("Invalid username, password.")
    def run(self):
        result = TestLib.APTQuery(self.testParameter)
        logging.info(result)
        return True if self.pattern.search(result) else False

class APT0203:
    def __init__(self):
        self.testParameter = {
                 'TEST_HOST': "10.1.168.63",
                 'TEST_PORT': 80,
                 'PROTOCOL_VER': '1',
                 'LICESE_ID' : 'apt_test_001',
                 'USERNAME' : 'apt_test',
                 'PASSWORD' : '5ks12%$----',
                 'SERVICE_TYPE' : '1',
                 'RESERVED' : '',
                 'DBG_FLAG' : '1',  
                 'QUERY_PARAMETER' : '1',
                 'QUERY_VALUE' : '203.70.58.177' 
        }
        self.pattern = re.compile("Invalid username, password.")
    def run(self):
        result = TestLib.APTQuery(self.testParameter)
        logging.info(result)
        return True if self.pattern.search(result) else False    

class APT0204:
    def __init__(self):
        self.url = testParameter['TEST_HOST']
        self.port = ''
        self.message = '/U0/88/3Yx4gBQgWnNaXI/Sng_GHQJMYIz_h6IlG8dDR7NnYH_0w6Cs_TU_H89kqoP3PqxFx6J3nF__hdAL4Ly9U_Oi3pg=='
        
    def run(self):
        result = TestLib.HTTPRequest(self.url, self.port, self.message)
        logging.info("status: {0}, reason: {1}".format(result.status, result.reason))
        return True if result.status == 404 else False    

class APT0205:
    def __init__(self):
        self.url = testParameter['TEST_HOST']
        self.port = ''
        self.message = '/U0/888/3Yx4gBQgWnNaXISng_GHQJMYIz_h6IlG8dDR7NnYH_0w6Cs_TU_H89kqoP3PqxFx6J3nF__hdAL4Ly9U_Oi3pg=='
        
    def run(self):
        result = TestLib.HTTPRequest(self.url, self.port, self.message)
        logging.info("status: {0}, reason: {1}".format(result.status, result.reason))
        return True if result.status == 404 else False

class APT0206:
    def __init__(self):
        self.url = testParameter['TEST_HOST']
        self.port = ''
        self.message = '/U0/AA/3Yx4gBQgWnNaXISng_GHQJMYIz_h6IlG8dDR7NnYH_0w6Cs_TU_H89kqoP3PqxFx6J3nF__hdAL4Ly9U_Oi3pg=='
        
    def run(self):
        result = TestLib.HTTPRequest(self.url, self.port, self.message)
        logging.info("status: {0}, reason: {1}".format(result.status, result.reason))
        return True if result.status == 404 else False 
    
class APT0207:
    def __init__(self):
        self.url = testParameter['TEST_HOST']
        self.port = ''
        self.message = '/U0/88/3Yx4gBQgWnNaXISng_GHQJMYIz_h6IlG8dDR7NnYH_0w6Cs_TU_H89kqoP3PqxFx6J3nF__hdAL4Ly9U_Oi3pg==ya'
        
    def run(self):
        result = TestLib.HTTPRequest(self.url, self.port, self.message)
        logging.info("status: {0}, reason: {1}".format(result.status, result.reason))
        return True if result.status == 404 else False    
    
class APT0208:
    def __init__(self):
        self.url = testParameter['TEST_HOST']
        self.port = ''
        self.message = '/U20/88/3Yx4gBQgWnNaXISng_GHQJMYIz_h6IlG8dDR7NnYH_0w6Cs_TU_H89kqoP3PqxFx6J3nF__hdAL4Ly9U_Oi3pg=='
        
    def run(self):
        result = TestLib.HTTPRequest(self.url, self.port, self.message)
        logging.info("status: {0}, reason: {1}".format(result.status, result.reason))
        return True if result.status == 405 else False

class APT0211:
    def __init__(self):
        self.url = testParameter['TEST_HOST']
        self.port = ''
        self.message = '/U20/88/3Yx4gBQgWnNaXISng_GHQJMYIz_h6IlG8dDR7NnYH_0w6Cs_TU_H89kqoP3PqxFx6J3nF__hdAL4Ly9U_Oi3pg==' * 100
        
    def run(self):
        result = TestLib.HTTPRequest(self.url, self.port, self.message)
        logging.info("status: {0}, reason: {1}".format(result.status, result.reason))
        return True if result.status == 405 else False


    
        
        