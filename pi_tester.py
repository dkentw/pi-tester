#!/usr/bin/python
# built-in
import os, sys
import logging
import ConfigParser
from optparse import OptionParser
# customize
import Engine.TestEngine as TestEngine
import Engine.parser as Parser
import Engine as engine


LOGGING_LEVELS = {'critical': logging.CRITICAL,
                  'error': logging.ERROR,
                  'warning': logging.WARNING,
                  'info': logging.INFO,
                  'debug': logging.DEBUG}

def main():
    parser = OptionParser(usage="usage: %prog [options][arg]")
    parser.add_option('-d', '--debug',
                      action='store', 
                      type='string', 
                      dest='debug_flag',
                      help='Turn on the debug mode [debug|info|warning|error]. Ex: $python threat_tester.py -d debug -c Dummy')
    parser.add_option('-c', '--caseid', 
                      action='store', 
                      type='string', 
                      dest="caseid_prefix", 
                      help="Run the specific test case by ID or prefix of test case ID.")
    parser.add_option('-s', '--csv', 
                      action='store', 
                      type='string', 
                      dest="run_csv_path", 
                      help="Run all test case in the specific csv file.")
    parser.add_option('-l', '--csvlist', 
                      action='store', 
                      type='string', 
                      dest="csv_list", 
                      help="Run all csv files via list in a file. It can exectue the csv by order from top to bottom.")
    parser.add_option('-a', '--all', 
                      action='store_true',  
                      dest="run_all_flag", 
                      help="Run all the test cases")
    parser.add_option("-g", "--gen", 
                      action='store',
                      type='string', 
                      dest="csv_file_path",
                      help="Generate the template of test scripts. Ex: $python threat_tester.py TestSuites/Dummy.csv")
    parser.add_option("-t", "--test", 
                      action='store_true', 
                      dest="test_flag",
                      default=False, 
                      help="For develope use")
    (options, args) = parser.parse_args()

    if options.debug_flag:
        # -d
        logLevel = LOGGING_LEVELS.get(options.debug_flag)
        logging.basicConfig(format='[%(levelname)-6s][%(name)s]:%(message)s', level=logLevel)
        logging.info("Turn on the debug mode!")
    else:
        logging.basicConfig(format='[%(levelname)-6s][%(name)s]:%(message)s', level=logging.WARN)
    
    if options.caseid_prefix:
        # -c
        runner = TestEngine.Runner(['all'])
        runner.run(options.caseid_prefix)     
    elif options.run_csv_path:
        # -s
        runner = TestEngine.Runner(options.run_csv_path.split(','))   
        runner.run_all()
    elif options.csv_list:
        # -l
        with open(options.csv_list, 'rb') as fh:
            for line in fh:
                csv_path = os.path.join('TestSuites', line.rstrip('\r\n'))
                runner = TestEngine.Runner([csv_path])   
                runner.run_all()
        
    elif options.csv_file_path:
        # -g
        arg = options.csv_file_path
        parser = Parser.TestCaseParser()
        testCaseSuites = parser.parse_from_csv([arg])
        TestEngine.GenerateTestCase(testCaseSuites)
    elif options.test_flag:
        # -t
        testCaseSuites, caseList, csvFileList = engine.ParseFromCSV()
        #Tester.GenerateTestCase(testCaseSuites, caseList, csvFileList)
    elif options.run_all_flag:
        # -a
        runner = TestEngine.Runner(['all'])
        runner.run_all()
    else:
        parser.print_help()
    
                   
if __name__ == "__main__":
    main()