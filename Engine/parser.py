'''
Created on 2012/6/24

@author: kent
'''
import os
import re
import logging
logger = logging.getLogger( 'Parser' )
import csv
import sys
import pprint
import json
import traceback

def get_csv_files():
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
    
    logger.info('[ParseFromCSV] CSV file list: {0}'.format(csvFilePaths))
    return csvFilePaths

class TestCaseParser:
    def __init__(self):
        pass
        
    def _verify_csv_format(self, csv_file):
        '''
        [TODO] this function maybe not work.
        :param fh csv_file_fh: file handle of csv 
        '''        
        try:
            with open(csv_file, 'rb') as csv_file_fh:
                try:
                    CSVSniffer = csv.Sniffer()
                    DiaObject = CSVSniffer.sniff(csv_file_fh.readline()) # this will flush the buffer of csv content
                except:
                    logger.error('[VerifyCSVFormat] [%s] CSVSniffer fail, is this a csv?' % csv_file)
                    csv_file_fh.close()
                    sys.exit(0)
                
                # Check format of CSV file is validate
                if DiaObject.delimiter == ',':
                    result = True
                else:
                    logger.error('[VerifyCSVFormat] [%s] Delimiter must be ","' % csv_file)
                    logger.error('Delimiter: ' + str(DiaObject.delimiter))
                    result = False
                    
                return result
        except IOError:
            logger.error('Fail to open file!')
            return False
        except:
            logger.error(traceback.format_exc())
            return False
            
    def _get_csv_content(self, csv_file_fh):
        '''
        :param fh csv_file_fh: file handle of csv
        '''
        try:
            csv_content = csv.reader(csv_file_fh, delimiter=',')
            logger.info(csv_content)
            result = csv_content
        except IOError as e:
            logger.error(e.strerror + ': ' + csv_file)
            result = False
        except csv.Error as e:
            logger.error('CSV file format error!')
            result = False
            
        return result
    
    def _extract_test_cases(self, case_classify, csv_content, csv_file):
        test_case_suite = {}
        ordered_cases = []
        test_case_suite[case_classify] = {}
        
        for row in csv_content:
            if csv_content.line_num == 1 :  # skip title
                continue
            
            if len(row) > 0: 
                case_id = row[1]
                case_run = row[4] 
                test_case_suite[case_classify].update({ case_id: {'run': case_run} })
                ordered_cases.append(case_id) # store test case id in list
        
        test_case_suite[case_classify]['ordered_cases'] = ordered_cases
        test_case_suite[case_classify]['csv_file_path'] = csv_file
        
        return test_case_suite 
        
    def parse_from_csv(self, test_case_suites):
        '''Parser CSV file and return the data with mapping structure, can parse 2 layers directory
        
        :return test_case_suite: 
        - test_case_suite: dict type, whole test case information
            Dummy: {
                    csv_file_path: "<path>"
                    ordered_cases: [Dummy001, Dummy002],
                    Dummy001: {
                                run: 1
                               }
                    },
                    Dummy002: {
                                run: 0
                               }
        '''
        logger.info('Start parsing the CSV file to test cases {0}'.format(test_case_suites))
        
        csv_files = []
        if test_case_suites[0] == 'all':
            csv_files = get_csv_files()
            logger.info('get csv files: %s' % str(csv_files))
        else:   
            # if test_case_suites is a known list
            working_folder = os.getcwd()
            for csv_file_path_related in test_case_suites:
                csv_files.append(os.path.join(working_folder, csv_file_path_related))

        # Parsing the CSV file
        test_case_suite = {}

        for csv_file in csv_files:
            if not self._verify_csv_format(csv_file):
                return False
            
            with open(csv_file, 'rb') as csv_file_fh:
                logger.info('[ParseFromCSV] real_csv_files: {0}'.format(csv_file))
                        
                csv_content = csv.reader(csv_file_fh, delimiter=',')
                temp_list = []
                if csv_content:
                    # Get the csv_content and handle it    
                    case_classify = os.path.basename(csv_file)[:-4]
                    test_case_suite.update( self._extract_test_cases(case_classify, csv_content, csv_file) )   

                else:
                    logger.warning('[ParseFromCSV][{0}] is not a CSV file with comma'.format(csv_file))
        
        logger.debug(str(test_case_suite))
        return test_case_suite
        