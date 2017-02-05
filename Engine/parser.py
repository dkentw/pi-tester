'''
Created on 2012/6/24

@author: kent
'''
import os
import logging
import csv
import sys
import traceback

logger = logging.getLogger('Parser')


def get_csv_files():
    '''Get all csv files in the working directory
    '''
    working_dir = os.getcwd()
    # testSuitesFolder = os.path.join(working_folder, 'TestSuites')
    # test_suites = os.listdir(testSuitesFolder)
    csv_files_path = []

    def find_csv_files(working_dir):
        item_list = os.listdir(working_dir)
        for item in item_list:
            if os.path.isdir(item):
                child_dir = os.path.join(working_dir, item)
                find_csv_files(child_dir)
            elif item[-3:] == 'csv':
                csv_files_path.append(os.path.join(working_dir, item))
            else:
                pass

    find_csv_files(working_dir)

    # ------
    # csvFilePaths = []
    # for entry1 in test_suites:
    #     entry1PathName = os.path.join(testSuitesFolder, entry1)
    #     if os.path.isdir(entry1PathName) == True:
    #         testSuites2Layer = os.listdir(entry1PathName)

    #         for entry2 in testSuites2Layer:
    #             entry2PathName = os.path.join(entry1PathName, entry2)
    #             if os.path.isdir(entry2PathName) == True:
    #                 logging.warning('[ParseFromCSV] There are folder in layer3 directory: {0}'.format(entry2PathName))
    #             else:
    #                 csvFilePaths.append(entry2PathName)
    #     else:
    #         csvFilePaths.append(entry1PathName)

    logger.info('[get_csv_files] CSV file list: {0}'.format(str(csv_files_path)))
    return csv_files_path


class TestCaseParser:
    def __init__(self):
        self.working_dir = os.getcwd()

    def _verify_csv_format(self, csv_file):
        '''
        [TODO] this function maybe not work.
        :param fh csv_file_fh: file handle of csv
        '''
        try:
            with open(csv_file, 'rb') as csv_file_fh:
                try:
                    CSVSniffer = csv.Sniffer()
                    DiaObject = CSVSniffer.sniff(csv_file_fh.readline())  # this will flush the buffer of csv content
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
            logger.error(traceback.print_exc())
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
            logger.error(e.strerror)
            result = False
        except csv.Error as e:
            logger.error('CSV file format error!')
            result = False

        return result

    def _extract_test_cases(self, case_classify, csv_content, csv_file):
        test_suites = {}
        ordered_cases = []
        test_suites[case_classify] = {}

        for row in csv_content:
            if csv_content.line_num == 1:  # skip title
                continue

            if len(row) > 0:
                case_id = row[1]
                case_run = row[4]
                test_suites[case_classify].update({case_id: {'run': case_run}})
                ordered_cases.append(case_id)  # store test case id in list

        test_suites[case_classify]['ordered_cases'] = ordered_cases
        test_suites[case_classify]['csv_file_path'] = csv_file

        return test_suites

    def parse_from_csv(self, test_suites=None):
        '''Parser CSV file and return the data with mapping structure, can parse 2 layers directory

        :return test_case_suite:
        - test_case_suite: dict type, whole test case information
            Dummy: {
                    csv_file_path: "<path>",
                    ordered_cases: [Dummy001, Dummy002],
                    Dummy001: { run: 1 },
                    Dummy002: { run: 0 }
        '''
        logger.info('Start parsing the CSV file to test cases {0}'.format(test_suites))

        csv_files = []
        if test_suites is None:
            csv_files = get_csv_files()
            logger.info('get csv files: %s' % str(csv_files))
        elif type(test_suites) == list:
            csv_files = test_suites
            logger.info('get csv files: %s' % str(csv_files))
        else:
            csv_files.append(test_suites)
            logger.info('get csv files: %s' % str(csv_files))

        full_test_cases = {}
        for csv_file in csv_files:
            if not self._verify_csv_format(csv_file):
                return False

            with open(csv_file, 'rb') as csv_file_fh:
                logger.info('[parse_from_csv] real_csv_files: {0}'.format(csv_file))

                csv_content = csv.reader(csv_file_fh, delimiter=',')
                if csv_content:
                    case_classify = os.path.basename(csv_file)[:-4]
                    full_test_cases.update(self._extract_test_cases(case_classify, csv_content, csv_file))
                else:
                    logger.warning('[parse_from_csv][{0}] is not a CSV file with comma'.format(csv_file))

        logger.debug('[parse_from_csv] all test cases: {0}'.format(full_test_cases))
        return full_test_cases


if __name__ == '__main__':
    pass

