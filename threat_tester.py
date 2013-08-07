#!/usr/bin/python
# built-in
import os, sys
import logging
import ConfigParser
from optparse import OptionParser
# customize
import Engine.TestEngine as Tester
import Engine as engine

LOGGING_LEVELS = {'critical': logging.CRITICAL,
                  'error': logging.ERROR,
                  'warning': logging.WARNING,
                  'info': logging.INFO,
                  'debug': logging.DEBUG}

config = ConfigParser.ConfigParser()
config.read('config.cfg')
#logging.basicConfig(format='[%(levelname)-7s]:%(message)s', level=logging.ERROR)

def main():
    usage = "usage: %prog [options] arg1 arg2"
    parser = OptionParser(usage="usage: %prog [options]")
    parser.add_option('-d', '--debug',
                      action='store', 
                      type='string', 
                      dest='debug_flag',
                      help='Turn on the debug mode [debug|info|warning|error].')
    parser.add_option('-c', '--caseid', 
                      action='store', 
                      type='string', 
                      dest="caseid_prefix", 
                      help="Run the specific test case by ID or prefix of test case ID.")
    parser.add_option("-g", "--gen", 
                      action='store',
                      type='string', 
                      dest="csv_file_path",
                      help="Generate the template of test cases. ex: ./threat_tester.py TestSuites/Dummy.csv")
    parser.add_option("-t", "--test", 
                      action='store_true', 
                      dest="test_flag",
                      default=False, 
                      help="For developer")
    (options, args) = parser.parse_args()

    if options.debug_flag:
        logLevel = LOGGING_LEVELS.get(options.debug_flag)
        logging.basicConfig(format='[%(levelname)-7s]:%(message)s', level=logLevel)
        logging.info("Turn on the debug mode!")
    else:
        logging.basicConfig(format='[%(levelname)-7s]:%(message)s', level=logging.ERROR)
    
    if options.caseid_prefix:
        Tester.run(options.caseid_prefix)
        
    elif options.csv_file_path:
        arg = options.csv_file
        testCaseSuites, caseList, csvFileList = engine.ParseFromCSV(arg)
        engine.GenerateTestCase(testCaseSuites, caseList, csvFileList)
        
    elif options.test_flag:
        testCaseSuites, caseList, csvFileList = engine.ParseFromCSV()
        #Tester.GenerateTestCase(testCaseSuites, caseList, csvFileList)
    else:
        parser.print_help()
    
                   
if __name__ == "__main__":
    main()