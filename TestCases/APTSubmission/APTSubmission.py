import httplib, urllib
import dataset
import copy
import json
import pprint

'''
key name can't exceed 1k length
value can't exceed 1k length
'''
class APTSubmission0101:
    '''
    Test value size > 1GB
    '''    
    def __init__(self):
        self.fileSize = 1*1024*1024*1024
        self.massFile = '/home/charles/value_1G'
    def run(self):
        conn = httplib.HTTPConnection('127.0.0.1')
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        
        data = copy.deepcopy(dataset.data1)
        data['nodes']['1']['sha1'] = "A" * self.fileSize
        
        try:
            fh = open(self.massFile, 'wb')
            json.dump(data, fh)
            fh.close()
        except IOError as e:
            print e
            
        try:
            fh = open(self.massFile, 'r')
            conn.request("POST", "/submission/?action=add&submitter=roel&ori_source=sandcastle&response=true", fh, headers)
            fh.close()
        except IOError as e:
            print e
        
        res = conn.getresponse()
        if res.status == 200:
            print res.read()
            return True
        else:
            return False
       
class APTSubmission0102:
    '''
    Test mass file size = 1MB
    issue: key too large
    '''    
    def __init__(self):
        self.fileSize = 1*1024*1024        
        self.massFile = '/home/charles/massfile_1M'
        
    def run(self):
        conn = httplib.HTTPConnection('127.0.0.1')
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        
        data = copy.deepcopy(dataset.data1)
        data['nodes']['1']['sha1'] = "A" * self.fileSize
        
        try:
            fh = open(self.massFile, 'wb')
            json.dump(data, fh)
            fh.close()
        except IOError as e:
            print e
            
        try:
            fh = open(self.massFile, 'r')
            conn.request("POST", "/submission/?action=add&submitter=roel&ori_source=sandcastle&response=true", fh, headers)
            fh.close()
        except IOError as e:
            print e
        
        res = conn.getresponse()
        if res.status == 200:
            print res.read()
            return True
        else:
            print res.status, res.reason
            return False
    
class APTSubmission0103:
    '''
    Test value exceed 1KB
    issue: stay log_transaction
    '''
    def __init__(self):
        self.fileSize = 1*1024       
        self.massFile = '/home/charles/value_1K.json'
        
    def run(self):
        conn = httplib.HTTPConnection('127.0.0.1')
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        
        data = copy.deepcopy(dataset.data1)
        longString = 'A' * self.fileSize
        data['nodes']['1024'] = { 'ntype': 'IP', 'address': longString }
        
        try:
            fh = open(self.massFile, 'wb')
            json.dump(data, fh)
            fh.close()
        except IOError as e:
            print e
            
        try:
            fh = open(self.massFile, 'r')
            conn.request("POST", "/submission/?action=add&submitter=roel&ori_source=sandcastle&response=true", fh, headers)
            fh.close()
        except IOError as e:
            print e
        
        res = conn.getresponse()
        if res.status == 200:
            print res.read()
            return True
        else:
            print res.status, res.reason
            return False
    
class APTSubmission0104:
    '''
    Test 10000 keys
    '''
    def __init__(self):
        self.massFile = '/home/charles/keys_10000.json'
        
    def run(self):
        conn = httplib.HTTPConnection('127.0.0.1')
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        
        data = copy.deepcopy(dataset.data1)
        for num in range(10000):
            index = num + 1000
            data['nodes'][str(index)] = { 'ntype': 'IP', 'address': 'test2' + str(num) }
        
        try:
            fh = open(self.massFile, 'wb')
            json.dump(data, fh)
            fh.close()
        except IOError as e:
            print e
            
        try:
            fh = open(self.massFile, 'r')
            conn.request("POST", "/submission/?action=add&submitter=roel&ori_source=sandcastle&response=true", fh, headers)
            fh.close()
        except IOError as e:
            print e
        
        res = conn.getresponse()
        if res.status == 200:
            print res.read()
            return True
        else:
            print res.status, res.reason
            pprint.pprint(data)
            return False

class APTSubmission0105:
    '''
    Test length of key name exceed 1024B
    '''
    def __init__(self):
        self.massFile = '/home/charles/key_length_1024.json'
        
    def run(self):
        conn = httplib.HTTPConnection('127.0.0.1')
        headers = {"Content-type": "application/octet-stream", "Accept": "text/plain"}
        
        data = copy.deepcopy(dataset.data1)
        
        #for num in range(100):
        num = 1024
        index = 'A' * num
        data['nodes'][str(index)] = { 'ntype': 'IP', 'address': 'test2' + str(num)}
        
        try:
            fh = open(self.massFile, 'wb')
            json.dump(data, fh)
            fh.close()
        except IOError as e:
            print e
            
        try:
            fh = open(self.massFile, 'r')
            conn.request("POST", "/submission/?action=add&submitter=roel&ori_source=sandcastle&response=true", fh, headers)
            fh.close()
        except IOError as e:
            print e
        
        res = conn.getresponse()
        if res.status == 200:
            print res.read()
            return True
        else:
            print res.status, res.reason
            pprint.pprint(data)
            return False
        
class APTSubmission0106:
    '''
    Test length of key name exceed 1024B
    '''
    def __init__(self):
        self.massFile = '/home/charles/key_length_1024.json'
        
    def run(self):
        conn = httplib.HTTPConnection('127.0.0.1')
        headers = {"Content-type": "application/octet-stream", "Accept": "text/plain"}
        
        data = copy.deepcopy(dataset.data1)
        
        #for num in range(100):
        num = 10
        index = 'A' * num
        submitter = 'k' *8191
        data['nodes'][str(index)] = { 'ntype': 'IP', 'address': 'APTSubmission0106'}
        
        try:
            fh = open(self.massFile, 'wb')
            json.dump(data, fh)
            fh.close()
        except IOError as e:
            print e
            
        try:
            fh = open(self.massFile, 'r')
            conn.request("POST", "/submission/?action=add&submitter=" + submitter + "&ori_source=sandcastle&response=true", fh, headers)
            fh.close()
        except IOError as e:
            print e
        
        res = conn.getresponse()
        if res.status == 200:
            print res.read()
            return True
        else:
            print res.status, res.reason
            pprint.pprint(data)
            return False
