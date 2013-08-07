'''
Created on 2012/6/24

@author: kent
'''
import os
import re
import logging
import csv
import sys
import pprint
import simplejson as json

def Getcsv_fileList():
    '''Get file list of a folder, only support 2 layer of directory
    ''' 
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
    
    logging.info('[ParseFromCSV] CSV file list: {0}'.format(csvFilePaths))
    return csvFilePaths

class TestCaseParser:
    
    def _VerifyCSVFormat(self, csv_file):
        '''
        Verify the CSV file, if validated, it will return the CSV content object.
        '''
        lengthOfCSV = len(csv_file)
        if csv_file[lengthOfCSV-3:lengthOfCSV] != 'csv':
            logging.info('[VerifyCSVFormat] skip none csv file: {0}'.format(csv_file))
            return False
        else:
            logging.info('[VerifyCSVFormat] Read csv file: {0}'.format(csv_file))
            try:
                fh = open(csv_file, 'rb')
                logging.info('[VerifyCSVFormat] opened file <{0}>'.format(csv_file))
            except:
                logging.error('[VerifyCSVFormat] open file fail: <{0}>'.format(csv_file))
                print '[ParseFromCSV] open file fail: <{0}>'.format(csv_file)
                fh.close()
                sys.exit(0)
        
            try:
                CSVSniffer = csv.Sniffer()
                DiaObject = CSVSniffer.sniff(fh.read(1024))
            except:
                logging.error('[VerifyCSVFormat] CSVSniffer fail')
                fh.close()
                sys.exit(0)
            
            # Check format of CSV file is validate
            if DiaObject.delimiter == ',':
                try:
                    csv_content = csv.reader(open(csv_file, 'rb'), delimiter=',')
                except IOError as e:
                    print e.strerror + ': ' + csv_file
                    fh.close()
                    return False
                fh.close()
                return csv_content
            else:
                logging.error('[VerifyCSVFormat] Delimiter is not ","')
                fh.close()
                return False    
            
    def ParseFromCSV(self, testCaseSuite):
        '''Parser CSV file and return the data with mapping structure, can parse layer2 directory
        
        :rtype: 
        - test_case_suite: dict type, whole test case information
        { <File Name> : { 
                            <CaseID>: { 
                                        'CaseTitle': <value-string>,
                                        'run': <value-string>
                                      },
                        },
        }
        - CaseList: a dict include a list of test cases, the included list can keep the order in CSV file.
            {
                <test case name>: [test_case_id1, test_case_id2, ...],
                ...
            }
        - realcsv_fileList: a list of csv files
        '''
        logging.info('Start parsing the CSV file to test cases {0}'.format(testCaseSuite))
        
        csv_files = []
        if testCaseSuite == 'all':
            csv_files = Getcsv_fileList()
                    
        else:   # ParseFormCSV() can parsing a specific file or files
            working_folder = os.getcwd()
            csv_files.append(os.path.join(working_folder, testCaseSuite))
        
        # Parsing the CSV file
        test_case_suite = {}
        test_case = {}       
        real_csv_files = []        
        for csv_file in csv_files:
            csv_content = self._VerifyCSVFormat(csv_file)
            
            tempList = []
            if csv_content:
                # Get the csv_content and handle it    
                test_case_suite[csv_file] = {}
                for row in csv_content:
                    if csv_content.line_num == 1 :
                        continue
                    tempList.append(row[1]) # store test case id in list
                    test_case_suite[csv_file].update({row[1]: {'CaseTitle': row[1], 'run': row[4]}})   
                            
                real_csv_files.append(csv_file) # only include real csv type file
                test_case_name = os.path.basename(csv_file)[:-4]
                test_case[test_case_name] = tempList
            else:
                logging.warning('[ParseFromCSV][{0}] is not a CSV file with comma'.format(csv_file))
        
        # use pprint to help debug mass data
        #pprint.pprint(csv_files)
        #pprint.pprint(test_case_suite)
        #pprint.pprint(test_case)    
        logging.info('[ParseFromCSV] Updated real_csv_files: {0}'.format(real_csv_files))
        #print json.dumps(test_case)
        return test_case_suite, test_case, real_csv_files
        