'''
Created on 2012/6/24

@author: kent
'''
import os
import re
import logging
import traceback
import time
from importlib import import_module

from parser import TestCaseParser
from reporter import Reporter
from feedback import Feedback

logger = logging.getLogger('TestEngine')


class Runner:
    def __init__(self, test_suite_csv=None, task_id=None, xml_filename=None):
        parser = TestCaseParser()
        self.test_suites = parser.parse_from_csv(test_suite_csv)
        self.reporter = Reporter()
        self.feedback = Feedback(task_id)
        self.test_result = {}
        self.test_summary = {}

    def _store_csv_path(self, case_classify, csv_file_path):
        """Store the csv path into test_result dict.
        """
        if case_classify in self.test_result.keys():
            self.test_result[case_classify]['csv_file_path'] = csv_file_path

    def _store_result(self, case_classify, case_id, run_result, log_message, passed_num, failed_num, run_time):
        """Store result related information into test_result dict.
        """
        if run_result is True:
            run_result = 'Pass'
            passed_num += 1
        elif run_result == 'Error':
            run_result = 'Error'
            failed_num += 1
        elif run_result is False:
            failed_num += 1
        else:
            # this include "not run" case
            pass

        if case_classify not in self.test_result.keys():
            self.test_result[case_classify] = {}

        if 'result' not in self.test_result[case_classify].keys():
            self.test_result[case_classify]['result'] = {}

        self.test_result[case_classify]['result'].update({case_id: [str(run_result), log_message, str(run_time)]})
        logger.debug('Test Result: {0}'.format(str(run_result)))

        return passed_num, failed_num

    def _store_summary(self, case_classify, ran_cases, passed_cases, failed_cases, total_run_time):
        if case_classify in self.test_result.keys():
            self.test_result[case_classify]['summary'] = {
                'ran_cases': ran_cases,
                'passed_cases': passed_cases,
                'failed_cases': failed_cases,
                'total_run_time': total_run_time
            }
        return True

    def _replace_attribue_with_vaiablespool(self, obj):
        from Engine.config import VariablesPool
        for key in VariablesPool.__dict__.keys():
            if not re.match(r'_{2}', key):
                setattr(obj, key, getattr(VariablesPool, key))

    def _invoke_test_case(self, case_id):
        '''
        :returns: the test result, the log message, the running time
        :rtype: string, string, string
        '''
        start_time = time.time()
        try:
            case_classify = case_id.split('_')[0]
            # mod = __import__('{0}.{0}'.format(case_classify), fromlist=[case_id])
            mod = import_module('{0}.{0}'.format(case_classify))
            mod_class = getattr(mod, case_id)
            mod_class_inst = mod_class()
            self._replace_attribue_with_vaiablespool(mod_class_inst)
            run_result, log_message = getattr(mod_class_inst, 'run')()
            logger.debug('Run test case: {0}.{1}'.format(case_classify, case_id))
            end_time = time.time()
            run_time = end_time - start_time
            result = (run_result, log_message, int(run_time))

        except:
            logger.error('[RUN] {0}.{1}'.format(case_classify, case_id))
            logger.error('working directory: {0}'.format(os.getcwd()))
            logger.error(traceback.format_exc())
            end_time = time.time()
            run_time = end_time - start_time
            result = ('Error', str(traceback.format_exc()), int(run_time))

        return result[0], result[1], result[2]

    def run_all(self):
        self.run('.*')

    def run(self, specific_case_id):
        run_count = 0
        passed_num = 0
        failed_num = 0
        specific_case_id = '\w' if specific_case_id == '' else specific_case_id
        self.feedback.feedback_to_server(self.test_result)  # this can initial feedback server.

        if self.test_suites is False:
            return
        for case_classify in self.test_suites.keys():
            if case_classify is None:
                logger.error('Found a None case_classify!')
                continue

            total_run_time = 0
            for case_id in self.test_suites[case_classify]['ordered_cases']:
                # CaseID can support REGEX
                pattern = re.compile(specific_case_id)
                re_result = pattern.search(case_id)
                if re_result is None:  # skip test case
                    continue
                logger.debug('Pattern: {0}, Match case: {1}'.format(specific_case_id, case_id))

                # CSV can control which case could be run
                runable = self.test_suites[case_classify][case_id]['run']
                if runable == '1':     # filter run = 0
                    run_count += 1
                    try:
                        run_result, log_message, run_time = self._invoke_test_case(case_id)
                    except:
                        logger.error(traceback.format_exc())
                        continue

                    passed_num, failed_num = self._store_result(case_classify,
                                                                case_id,
                                                                run_result,
                                                                log_message,
                                                                passed_num, failed_num,
                                                                run_time)
                    total_run_time = total_run_time + run_time
                else:
                    self._store_result(case_classify, case_id, 'N/A', '', 0, 0, 0)

            else:
                csv_file_path = self.test_suites[case_classify]['csv_file_path']
                self._store_csv_path(case_classify, csv_file_path)  # save csv_file_path in test_result
                self._store_summary(case_classify, run_count, passed_num, failed_num, total_run_time)
                run_count = passed_num = failed_num = 0

        logger.debug('Test Result: %s' % str(self.test_result))

        try:
            self.feedback.feedback_to_server(self.test_result)
        except:
            logger.error(traceback.format_exc())
            logger.error('Please check the server configuration!')

        self.reporter.output_report(self.test_result)


def _write_template(script_filename_path, cases):
    if not os.path.exists(script_filename_path):    # Don't overwrite the test scripts
        fh = open(script_filename_path, 'w')
        if not fh:
            logger.error('Open file fail: {0}'.format(script_filename_path))

        for value in cases:
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
        fh.close()


def GenerateTestCase(test_suites):
    working_folder = os.getcwd()
    test_cases_dir = {'top_level': working_folder}
    init_file = os.path.join(test_cases_dir['top_level'], '__init__.py')

    if not os.path.exists(init_file):
        fh = open(init_file, 'w')
        fh.close()
        logger.info('[GenerateTestCase] create file {0}'.format(init_file))
    else:
        logging.info('[GenerateTestCase] The ini file is exist: {0}'.format(init_file))

    for case_classify in test_suites:
        file_path = test_suites[case_classify]['csv_file_path']
        file_name = os.path.basename(file_path)
        file_name_no_ext = file_name.split('.')[0]
        test_cases_dir['layer2'] = os.path.join(test_cases_dir['top_level'], file_name_no_ext)
        script_filename_path = os.path.join(test_cases_dir['layer2'], file_name_no_ext + '.py')

        logger.info('[GenerateTestCase] script_filename_path = {0}'.format(script_filename_path))

        if not os.path.isfile(script_filename_path):
            try:
                os.makedirs(test_cases_dir['layer2'])             # create layer2 folder
            except:
                logger.error('canot make dir {0}'.format(script_filename_path))
                pass

            fh = open(os.path.join(test_cases_dir['layer2'], '__init__.py'), 'w')
            logger.info('[GenerateTestCase] create file {0}'.format(init_file))
            fh.close()

            _write_template(script_filename_path, test_suites[case_classify]['ordered_cases'])
        else:
            logging.warning('[GenerateTestCase] -The file is exist, it will not write template:')
            logging.warning('[GenerateTestCase] -{0}'.format(script_filename_path))
