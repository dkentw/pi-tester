'''
Created on 2012/6/24

@author: kent
'''
import os
import re
import logging
logger = logging.getLogger('Engine')
import csv
import sys
import pprint
import simplejson as json

from parser import TestCaseParser
from reporter import Reporter
#logger = logging.getLogger('TestEngine')
#logger.setLevel(logging.INFO)
#logging.basicConfig(level=logging.INFO)
#logging.getLogger('Threat')        
        


'''
def ReadTestSuites():
    config = ConfigParser.RawConfigParser()
    try:
        config.read('TestSuites/AptInfoServiceSuites.cfg')
    except:
        print 'it can\'t read test suites file'
    mySections = config.sections()
    return mySections
'''   
        
def run(caseID):
    '''
    Execute the test cases
    '''
    reporter = Reporter()
    parser = TestCaseParser()
    logger.info('Start to handle the test cases')
    
    # Parse test cases form CSV
    test_case_suite, test_case_list, csv_files = parser.ParseFromCSV('all')
    logger.info('[run] Test cases List: {0}'.format(test_case_list))
    #logger.info(testCases)
    #pprint.pprint(test_case_suite)
    #pprint.pprint(test_case_list)
    #pprint.pprint(csv_files)
    
    if not test_case_list:
        print "Test cases list is empty or didn't read any data!"
        return True
    
    run_count = 0
    passed_num = 0
    failed_num = 0
    caseID = '\w' if caseID == '' else caseID
        
    for testCaseClassify in test_case_list.keys():
        for test_case_id in test_case_list[testCaseClassify]:
            # CaseID can support regex
            pattern = re.compile(caseID)            
            re_result = pattern.search(test_case_id)
            if re_result == None:                        # filter prefix
                continue
            
            # TestCaseSuites can control which case could be run 
            working_folder = os.getcwd()
            testSuitesFolder = os.path.join(working_folder, 'TestSuites')
            csvFileName = os.path.join(testSuitesFolder, testCaseClassify) + '.csv'
            
            if test_case_suite[csvFileName][test_case_id]['run'] == '1':     # filter run = 0
                run_count += 1                
                testScript = testCaseClassify
                try:
                    mod = __import__('TestCases.{0}.{0}'.format(testScript), fromlist=[test_case_id])
                    testCaseClass = getattr(mod, test_case_id)
                    myTestCase = testCaseClass()
                    test_result, log_message = getattr(myTestCase, 'run')()
                    
#                     logger.info("[{0}]".format(test_case_id))
#                     logger.info("[Test Result]: {0}, {1}".format(test_result, log_message))
#                     logger.info("-"*60)
                    
                except (AttributeError, TypeError) as e:
                    test_result = False
                    
                    logging.error('TestCases.{0}.{1}'.format(testScript, test_case_id))
                    print e            
                    
                #----save result
                if test_result == True:
                    reporter.save_result(testCaseClassify, test_case_id, 'Pass', log_message)
                    passed_num += 1
                else:
                    reporter.save_result(testCaseClassify, test_case_id, 'Fail', log_message)
                    failed_num += 1
        else:            
            reporter.save_summary(testCaseClassify, run_count, passed_num, failed_num)
            run_count = passed_num = failed_num = 0
            
    reporter.ShowReport()  

    
def GetCSVFileList():
    # Get file list of a folder, only support 2 layer of directory 
    working_folder = os.getcwd()
    testSuitesFolder = os.path.join(working_folder, 'TestSuites')
    test_suites = os.listdir(testSuitesFolder)
    csvFilePaths = []
    for entry1 in test_suites:
        entry1PathName = os.path.join(testSuitesFolder, entry1)
        if os.path.isdir(entry1PathName) == True:
            testSuites2Layer = os.listdir(entry1PathName)    
            
            for entry2 in testSuites2Layer:
                entry2PathName = os.path.join(entry1PathName, entry2)    
                if os.path.isdir(entry2PathName) == True:
                    logging.warning('[ParseFromCSV] There are folder in layer3 directory: {0}'.format(entry2PathName))
                else:
                    csvFilePaths.append(entry2PathName)
        else:
            csvFilePaths.append(entry1PathName)
    
    logger.info('[ParseFromCSV] CSV file list: {0}'.format(csvFilePaths))
    return csvFilePaths
    
    

def WriteTemplate(testCaseFileNamePath, TestCase_dict, testCases):
    fh = open(testCaseFileNamePath, 'w')
    if not fh:
        print('Open file fail: {0}'.format(testCaseFileNamePath))
        
        
    testCaseFileName = os.path.basename(testCaseFileNamePath)
    fileNameNoExt = testCaseFileName[0:-3]
    for value in TestCase_dict[fileNameNoExt]:
        temp = '''
class {0}:
    \'\'\'
    write doc here
    \'\'\'    
    def __init__(self):
        pass
    def run(self):
        return False, \'\'
    '''.format(value)
        fh.write(temp)
        #print temp
    fh.close()
    #print temp
    #pprint.pprint(testCases)
    
def GenerateTestCase(test_case_suite, TestCase_dict, csv_files):
    working_folder = os.getcwd()
    TestCase_dir = {'top_level': os.path.join(working_folder, 'TestCases')}
    initFileName = os.path.join(TestCase_dir['top_level'], '__init__.py')
    
    if not os.path.exists(initFileName):
        fh = open(initFileName, 'w')
        logger.info('[GenerateTestCase] create file {0}'.format(initFileName))
        fh.close()
    else:
        logging.warning('[GenerateTestCase] The ini file is exist: {0}'.format(initFileName))
    
    for fileNamePath in csv_files:
        fileName = os.path.basename(fileNamePath)
        fileNameNoExt = fileName.split('.')[0]
        TestCase_dir['layer2'] = os.path.join(TestCase_dir['top_level'], fileNameNoExt)
        testCaseFileNamePath = os.path.join(TestCase_dir['layer2'], fileNameNoExt + '.py')
        
        logger.info('[GenerateTestCase] testCaseFileNamePath = {0}'.format(testCaseFileNamePath))
        
        if not os.path.isfile(testCaseFileNamePath):
            try:
                os.makedirs(TestCase_dir['layer2'])             # create layer2 folder
            except:
                print '[Error][C]: canot make dir {0}'.format(testCaseFileNamePath)
                pass
                
            fh = open(os.path.join(TestCase_dir['layer2'], '__init__.py'), 'w')
            logger.info('[GenerateTestCase] create file {0}'.format(initFileName))
            fh.close()
            
            WriteTemplate(testCaseFileNamePath, TestCase_dict, test_case_suite)                    
        else:
            logging.warning('[GenerateTestCase] -The file is exist, it will not write template:') 
            logging.warning('[GenerateTestCase] -{0}'.format(testCaseFileNamePath))
    
    
        
        
        