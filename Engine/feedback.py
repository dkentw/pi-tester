import sys
import logging
logger = logging.getLogger('Feedback')
import traceback
import json
import urllib2
import urllib

class Feedback:
    def __init__(self):
        from pi_config import FEEDBACK_SERVER
        from pi_config import CLIENT
        
        self.server_url = FEEDBACK_SERVER['server_url']
        self.reports_url = self.server_url + FEEDBACK_SERVER['reports_path']
        self.status_url = self.server_url + FEEDBACK_SERVER['status_path']
        self.hostname = CLIENT['hostname']
        #---check if server alive
        try:
            response = urllib2.urlopen(self.server_url, timeout=1)
            self.server_down = False
        except:
            logger.warn('It can not connect to feedback server!')
            self.server_down = True
        
    def _notify_running(self):
        # init the statistic of dashboard
        request = { "statistic": json.dumps([0,0,0,0,1]), "hostname": self.hostname}
        encode_data = urllib.urlencode(request)
        
        try:
            response = urllib2.urlopen(self.status_url, encode_data)
        except:
            response = None
            logger.error(traceback.format_exc())
            logger.error('Network configuration may be wrong!')
        
        logger.debug('[notify_running]: %s' % response)
    
    def _notify_end(self, test_summary):
        pass
    
    def _feedback_reports(self, test_result):
        #data = 'data=\"%s\",hostname=\"%s\"' % (str(test_result), self.hostname)
        
        request = { "data": json.dumps(test_result), "hostname": self.hostname}
        encode_data = urllib.urlencode(request)
        
        logger.debug('url: %s' % self.reports_url)
        logger.debug('data: %s' % encode_data)
        
        try:
            response = urllib2.urlopen(self.reports_url, encode_data)
        except:
            response = None
            logger.error(traceback.format_exc())
            logger.error('Network configuration may be wrong!')
            
        logger.debug('[feedback_report]: %s' % response)
    
    def feedback_to_server(self, test_result):
        if self.server_down is False:
            if test_result == {}:
                self._notify_running()
            else:
                self._feedback_reports(test_result)