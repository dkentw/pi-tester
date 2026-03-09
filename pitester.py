#!/usr/bin/python
import os
import sys
import logging
import argparse
import re

import Engine.TestEngine as TestEngine
import Engine.parser as Parser
import Engine as engine
from Engine.config import VariablesPool


LOGGING_LEVELS = {'critical': logging.CRITICAL,
                  'error': logging.ERROR,
                  'warning': logging.WARNING,
                  'info': logging.INFO,
                  'debug': logging.DEBUG}


def parse_variable(variables):
    if re.fullmatch(r'\w+:[^,]+(,\w+:[^,]+)*', variables):
        variable_dict = {}
        variable_list = variables.split(',')

        for vairable in variable_list:
            variable_pair = vairable.split(':')
            variable_dict.update({variable_pair[0]: variable_pair[1]})
            setattr(VariablesPool, variable_pair[0], variable_pair[1])
    else:
        raise Exception('The format of the string to variable is wrong.')


def main():
    sys.path.append(os.getcwd())
    parser = argparse.ArgumentParser(usage="%(prog)s [options][arg]")
    parser.add_argument('-d', '--debug',
                        dest='debug_flag',
                        help='Turn on the debug mode [debug|info|warning|error]. Ex: $python pitester.py -d debug -c Dummy')
    parser.add_argument('-c', '--caseid',
                        dest="caseid_prefix",
                        help="Run the specific test case by ID or prefix of test case ID.")
    parser.add_argument('-s', '--csv',
                        dest="run_csv_path",
                        help="Run all test case in a specific csv file.")
    parser.add_argument('-l', '--csvlist',
                        dest="csv_list",
                        help="Run all csv files via list in a file. It can exectue the csv by order from top to bottom.")
    parser.add_argument('-a', '--all',
                        action='store_true',
                        dest="run_all_flag",
                        help="Run all the test cases")
    parser.add_argument("-g", "--gen",
                        dest="csv_file_path",
                        help="Generate the template of test scripts. Ex: $python pitester.py -g TestSuites/Dummy.csv")
    parser.add_argument("-t", "--test",
                        action='store_true',
                        dest="test_flag",
                        default=False,
                        help="For develope use")
    parser.add_argument("-x", "--xml",
                        dest="xml_filename",
                        help="Output the xml file with junit xml format.")
    parser.add_argument("-v", "--variables",
                        dest="variables",
                        help="Variables with 'var1:AAA,var2:BBB'")
    options = parser.parse_args()

    if options.variables:
        parse_variable(options.variables)

    if options.debug_flag:
        # -d
        if options.debug_flag not in LOGGING_LEVELS.keys():
            raise Exception('Invalid log level.')
        log_level = LOGGING_LEVELS.get(options.debug_flag)
        logging.basicConfig(format='[%(levelname)-6s][%(name)s]:%(message)s', level=log_level)
        logging.info("Turn on the debug mode!")
    else:
        logging.basicConfig(format='[%(levelname)-6s][%(name)s]:%(message)s', level=logging.WARN)

    if options.caseid_prefix:
        # -c
        runner = TestEngine.Runner(xml_filename=options.xml_filename)
        runner.run(options.caseid_prefix)
    elif options.run_csv_path:
        # -s
        runner = TestEngine.Runner(test_suite_csv=options.run_csv_path, xml_filename=options.xml_filename)
        runner.run_all()
    elif options.csv_list:
        # -l
        with open(options.csv_list, 'r') as fh:
            for line in fh:
                run_csv_path = line.rstrip('\r\n')
                runner = TestEngine.Runner(test_suite_csv=run_csv_path, xml_filename=options.xml_filename)
                runner.run_all()

    elif options.csv_file_path:
        # -g
        arg = options.csv_file_path
        csv_parser = Parser.TestCaseParser()
        testCaseSuites = csv_parser.parse_from_csv([arg])
        TestEngine.GenerateTestCase(testCaseSuites)
    elif options.test_flag:
        pass
        # -t
        # Tester.GenerateTestCase(testCaseSuites, caseList, csvFileList)
    elif options.run_all_flag:
        # -a
        runner = TestEngine.Runner()
        runner.run_all()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
