'''
Created on 2013/7/3

@author: kent
'''
import os
import sys
import time
import pprint
import logging
import csv

logger = logging.getLogger(__name__)


class Reporter:
    def __init__(self):
        self.summary = {}
        self.ran_cases = 0
        self.passed_cases = 0
        self.failed_cases = 0
        self.html_template = ''
        self.report_create_time = 'XX'
        
    def _create_html_head(self):
        html_head = ' \
            <meta charset="utf-8" /> \
            <meta http-equiv="X-UA-Compatible" content="IE=edge,chrome=1" /> \
            <meta name="description" content="" /> \
            <meta name="author" content="kent chen" /> \
            <meta name="viewport" content="width=device-width; initial-scale=1.0" /> \
            <link href="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.3.2/css/bootstrap-combined.min.css" rel="stylesheet"> \
            <script src="http://netdna.bootstrapcdn.com/twitter-bootstrap/2.3.2/js/bootstrap.min.js"></script>'
        return html_head
        
    def _create_summary_table(self, case_classify, test_summary):
        if not test_summary:
            html_table =''
        else:
            html_table = ' \
                <table class="table table-hover table-bordered" style="width:200px"> \
                <tbody> \
                <tr class="info"><td>Ran Cases</td><td><strong>%s</strong></td></tr> \
                <tr class="success"><td>Passed</td><td><strong>%s</strong></td></tr> \
                <tr class="error"><td>Failed</td><td><strong>%s</strong></td></tr> \
                </tbody> \
                </table>' % (test_summary['ran_cases'], test_summary['passed_cases'], test_summary['failed_cases']) 
        return html_table
        
    def _create_html_table(self, test_result):
        table_body_content = ''
        keys = test_result.keys()
        keys.sort()
        for case_id in keys:
            if test_result[case_id][0] == 'Fail':
                table_body_content =  table_body_content + \
                                      '<tr><td>%s</td><td style="background-color:#F2DEDE">%s</td><td>%s</td><td>%s</td></tr>' % \
                                      (case_id, str(test_result[case_id][0]), str(test_result[case_id][1]), str(test_result[case_id][2]))
            else:
                table_body_content =  table_body_content + \
                                      '<tr><td>%s</td><td style="background-color:#D0E9C6">%s</td><td>%s</td><td>%s</td></tr>' % \
                                      (case_id, str(test_result[case_id][0]), str(test_result[case_id][1]), str(test_result[case_id][2]))      

        html_table = ' \
            <table class="table table-hover"> \
            <thead><tr><th>Case ID</th><th>Test Result</th><th>Log Message</th><th>Duration Time</th></tr></thead> %s \
            </table>' % table_body_content

        return html_table
    
    def _create_report_file(self, filename, content):
        root_dir = os.getcwd()
        reports_dir = root_dir + '/Reports/' + self.report_create_time + '/'
        report_file_name = reports_dir + filename + '.html'
        
        if not os.path.exists(reports_dir):
            os.mkdir(reports_dir)
            
        with open(report_file_name, 'wb') as fh:
            fh.write(content)
            
    def _generate_html_file(self, case_classify, test_result, test_summary):
        head = self._create_html_head()
        table = self._create_html_table(test_result)
        summary_table = self._create_summary_table(case_classify, test_summary)
        style = 'div#main {width: 90%; margin: auto}'

        html = '''
<html>
    <head>
        <style>%s</style>
        <title>%s</title>
        %s
    </htad>
    <body>
        <div id="main">
            <h1>%s</h1>
            <hr>
            <h3>Summary</h3>
            %s
            <hr>
            <h3>Detail</h3>
            %s
        </div>
    </body>
</html>
        ''' % (style, case_classify, head, case_classify, summary_table, table)
        
        root_dir = os.getcwd()
        reports_root_dir = root_dir + '/Reports/'
        reports_dir = reports_root_dir + self.report_create_time + '/'
        report_file_name = reports_dir + case_classify + '.html'
        
        if not os.path.exists(reports_root_dir):
            os.mkdir(reports_root_dir)
        if not os.path.exists(reports_dir):
            os.mkdir(reports_dir)
            
        with open(report_file_name, 'wb') as fh:
            fh.write(html)
            
    def _generate_summary_html_file(self, test_summary):
        summary_table = ''
        total_pass = 0
        total_fail = 0
        total_ran = 0
        for case_classify in test_summary:
            total_pass = total_pass + test_summary[case_classify]['passed_cases']
            total_fail = total_fail + test_summary[case_classify]['failed_cases']
            total_ran = total_ran + test_summary[case_classify]['ran_cases']
            summary_table = summary_table + \
                            '<tr><td>%s</td><td style="background-color:#D0E9C6">%s</td><td style="background-color:#F2DEDE">%s</td><td>%s</td></tr>' % \
                            ( case_classify, 
                              str(test_summary[case_classify]['passed_cases']), 
                              str(test_summary[case_classify]['failed_cases']), 
                              str(test_summary[case_classify]['ran_cases'])
                            )
        
        html_table = ' \
            <table class="table table-hover"> \
            <thead><tr><th>Classify<th>Pass</th><th>Fail</th><th>Ran Cases</th></tr></thead> %s \
            <tfoot><tr><td>Total</td><td>%s</td><td>%s</td><td>%s</td></tr></tfoot> \
            </table>' % (summary_table, str(total_pass), str(total_fail), str(total_ran))
                        
        head = self._create_html_head()
        style = 'div#main {width: 90%; margin: auto} tfoot { font-weight:bold }'

        html_code = '''
<html>
    <head>
        <style>%s</style>
        <title>Total Summary Result</title>
        %s
    </htad>
    <body>
        <div id="main">
            <h1>Summary</h1>
            %s
        </div>
    </body>
</html>
        ''' % (style, head, html_table)
        
        self._create_report_file('SummaryReport', html_code)
                    
    
    def _output_result_to_csv(self, test_result):
        import shutil
        csv_content = []
        for case_classify in test_result.keys():
            csv_file_path = test_result[case_classify]['csv_file_path']
            csv_file_path_backup = csv_file_path + '.backup' 
            shutil.copy(csv_file_path, csv_file_path_backup)
            
            with open(test_result[case_classify]['csv_file_path'], 'rb') as fh:
                csv_content = [row for row in csv.reader(fh, delimiter=',')]
                
            for index, row in enumerate(csv_content):
                if index != 0:
                    case_id = csv_content[index][1]
                    if case_id in test_result[case_classify]['result'].keys():
                        csv_content[index][5] = test_result[case_classify]['result'][case_id][0]
                        csv_content[index][6] = test_result[case_classify]['result'][case_id][1]
                        csv_content[index][7] = test_result[case_classify]['result'][case_id][2]
            
            with open(test_result[case_classify]['csv_file_path'], 'wb') as fh:
                csv_writer = csv.writer(fh, delimiter=',')
                try:
                    for row in csv_content:
                        csv_writer.writerow(row)
                    os.remove(csv_file_path_backup) # remove the backup if update csv success.
                except:
                    logger.error('Output to csv file fail!')
    
    def _get_summary_dict(self, test_result):
        summary_dict = {}
        for classify in test_result:
            summary_dict[classify] = { 
                                    "passed_cases": test_result[classify]['summary']['passed_cases'],
                                    "failed_cases": test_result[classify]['summary']['failed_cases'],
                                    "ran_cases": test_result[classify]['summary']['ran_cases']
                                   }
            
        return summary_dict
        
    def output_report(self, test_result):
        if test_result == {}:
            print '[what?!] there are not any test result, what is the test case id?'
        else:
            print 
            summary_dict = self._get_summary_dict(test_result)
            self.report_create_time = str(time.strftime('%Y%m%d_%H%M%S', time.localtime()))
            for case_classify in test_result.keys():
                if test_result[case_classify].has_key('result'):
                    # Generate HTML report
                    self._generate_html_file(case_classify, test_result[case_classify]['result'], test_result[case_classify]['summary'])
                
                    # Save the result into the CSV
                    self._output_result_to_csv(test_result)
                
                    # Show in Console
                    print '{0} {1} {2}'.format('='*16, case_classify, '='*16)
                    test_case_result = test_result[case_classify]['result']
                    for case_id in test_case_result.keys():                    
                        print '[{0}][{1}] {2}, {3}, {4}'.format(case_classify, case_id, test_case_result[case_id][0], test_case_result[case_id][1], str(test_case_result[case_id][2]))
                
            self._generate_summary_html_file(summary_dict)
            print '{0} {1} {2}'.format('='*16, 'Summary', '='*16)
            pprint.pprint(summary_dict)
