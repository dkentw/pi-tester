'''
Created on 2013/7/3

@author: kent
'''
import os
import sys
import pprint

from lxml import etree
from lxml.html import builder as E
import lxml.html

class Reporter:
    def __init__(self):
        self.test_result = {}
        self.summary = {}
        self.ran_cases = 0
        self.passed_cases = 0
        self.failed_cases = 0
        self.html_template = ''
        
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
        
    def _create_summary_table(self, test_category):
        html_table = ' \
            <table class="table table-hover table-bordered" style="width:200px"> \
            <tbody> \
            <tr class="info"><td>Ran Cases</td><td><strong>%s</strong></td></tr> \
            <tr class="success"><td>Passed</td><td><strong>%s</strong></td></tr> \
            <tr class="error"><td>Failed</td><td><strong>%s</strong></td></tr> \
            </tbody> \
            </table>' % (self.summary[test_category]['ran_cases'], self.summary[test_category]['passed_cases'], self.summary[test_category]['failed_cases']) 
        return html_table
        
    def _create_html_table(self, test_result):
        table_body_content = ''
        keys = test_result.keys()
        keys.sort()
        for case_id in keys:
            if test_result[case_id][0] == 'Fail':
                table_body_content =  table_body_content + '<tr><td>' + case_id + '</td><td style="background-color:#F2DEDE">' + test_result[case_id][0] + '</td><td>' + test_result[case_id][1] + '</td></tr>'
            else:
                table_body_content =  table_body_content + '<tr><td>' + case_id + '</td><td style="background-color:#D0E9C6">' + test_result[case_id][0] + '</td><td>' + test_result[case_id][1] + '</td></tr>'       

        html_table = ' \
            <table class="table table-hover"> \
            <thead><tr><th>Case ID</th><th>Test Result</th><th>Log Message</th></tr></thead> %s \
            </table>' % table_body_content

        return html_table
    
    
    def _generate_html_file(self, test_category, test_result):
        head = self._create_html_head()
        table = self._create_html_table(test_result)
        summary_table = self._create_summary_table(test_category)

        html = E.HTML(
                        E.HEAD( 
                                E.STYLE('div {width: 90%; margin: auto}'),
                                E.TITLE(test_category),
                                lxml.html.fromstring(head) 
                                ),
                        E.BODY(
                                E.DIV(
                                      E.H1(E.CLASS('text-center'), test_category),
                                      E.HR(),
                                      E.H3('Summary'),
                                      lxml.html.fromstring(summary_table),
                                      E.HR(),
                                      E.H3('Detail'), 
                                      lxml.html.fromstring(table) 
                                ))
                      )
        
        root_dir = os.getcwd()
        reports_dir = root_dir + '/Reports/'
        report_file_name = reports_dir + test_category + '.html'
        
        if not os.path.exists(reports_dir):
            os.mkdir(reports_dir)
            
        with open(report_file_name, 'wb') as fh:
            fh.write(lxml.html.tostring(html))            
            
            
        return
    
    def save_result(self, testCaseClassify, test_case_id, test_result, log_message):
        if not self.test_result.has_key(testCaseClassify):
            self.test_result[testCaseClassify] = {}
        
        self.test_result[testCaseClassify].update({ test_case_id: (test_result, log_message)})
        return True
    
    def save_summary(self, testCaseClassify, ran_cases, passed_cases, failed_cases):
        self.summary[testCaseClassify] = {
                                            'ran_cases': ran_cases,
                                            'passed_cases': passed_cases,
                                            'failed_cases': failed_cases 
                                          }
        return True
    
    def output_report(self):
        root_dir = os.getcwd()
        reports_dir = root_dir + '/Reports/'
        if not os.path.isdir(reports_dir):
            os.mkdir(reports_dir)
            
        for test_case_classify in self.test_result:
            log_file_name = reports_dir + test_case_classify + '.txt'
            with open(log_file_name, 'wb') as logfile:
                for test_case_id, test_result_tuple in self.test_result[test_case_classify].items():
                    log_str = test_case_id + '\t' + test_result_tuple[0] + '\t' + test_result_tuple[1] + '\n'
                    logfile.write(log_str)
    
    def ShowReport(self):       # for stdout
        #self.output_report()
        
        if self.test_result == {}:
            print 'what?! there are not any test result, what is the test case id?'
        else:
            print 
            for test_category in self.test_result:
                self._generate_html_file(test_category, self.test_result[test_category])
                for case_id in self.test_result[test_category]:
                    print '[{0}][{1}] {2}, {3}'.format(test_category, case_id, self.test_result[test_category][case_id][0], self.test_result[test_category][case_id][1])
                
            print '=========== Summary ================'
            pprint.pprint(self.summary)
