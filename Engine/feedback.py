import logging
import traceback
import json
import urllib2
import urllib
import socket

logger = logging.getLogger('Feedback')


class Feedback:
    def __init__(self, task_id):
        from config import FEEDBACK_SERVER

        self.task_id = task_id
        self.server_url = FEEDBACK_SERVER['server_url']
        self.reports_url = self.server_url + FEEDBACK_SERVER['reports_path']
        self.status_url = self.server_url + FEEDBACK_SERVER['status_path']
        self.hostname = socket.gethostname()
        try:
            urllib2.urlopen(self.server_url, timeout=1)
            self.server_down = False
        except:
            logger.warn('It can not connect to feedback server!')
            self.server_down = True

    def _notify_running(self):
        """statistic: [passed, failed, error, total_ran, run_time, run_status]
        """
        request = {"statistic": json.dumps([0, 0, 0, 0, 0, 1]), "hostname": self.hostname, "task_name": self.task_id}
        encode_data = urllib.urlencode(request)

        # data = 'dashboard={"hostname":"%s","statistic":[0,0,0,1]}' % self.hostname
        try:
            response = urllib2.urlopen(self.status_url, encode_data)
        except:
            response = None
            logger.error('Network configuration may be wrong!')
            logger.error('Server url: %s' % self.status_url)
            logger.error('Send data: %s' % str(encode_data))
            logger.error(traceback.format_exc())

        logger.debug('[notify_running]: %s' % response)

    def _notify_end(self, test_summary):
        pass

    def _feedback_reports(self, test_result):
        #data = 'data=\"%s\",hostname=\"%s\"' % (str(test_result), self.hostname)

        request = { "data": json.dumps(test_result), "hostname": self.hostname, "task_id": self.task_id}
        encode_data = urllib.urlencode(request)

        logger.debug('url: %s' % self.reports_url)
        logger.debug('data: %s' % request)

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
                # start running
                self._notify_running()
            else:
                # finished the test
                self._feedback_reports(test_result)