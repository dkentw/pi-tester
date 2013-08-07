#!/usr/bin/env python

import os
import sys
import memcache
import logging

import time
from hashlib import sha1
import pprint

sys.path.append(os.path.join(os.path.dirname(__file__), '..')) # for settings
import settings

_last_error_str = ""
_last_error_log_time = 0
_NO_REPEAT_LOG_TIME = 60 # seconds

def memcache_debuglog(self, error_str):
    # No repeat log in 60 seconds.
    global _last_error_str
    global _last_error_log_time
    
    now_time = time.time()
    if _last_error_str == error_str:
        if now_time - _last_error_log_time < _NO_REPEAT_LOG_TIME:
            return
    _last_error_log_time = now_time
    _last_error_str = error_str
    logging.error('[memcache_error] %s'%(error_str))

# set debug output to python logging.
memcache.Client.debuglog = memcache_debuglog

def do_flush(cli):
    cli.flush_all()

def do_stats(cli):
    stats_list = cli.get_stats()
    
    def pick_stats(stats, stats_name):
        return '%s: [%7s]'%(stats_name, stats[1][stats_name])
    
    
    for stats in stats_list:
        picked_stats_list = []
        #picked_stats_list.append('== %s ========================'%(stats[0]))
        picked_stats_list.append('%s:'%(stats[0]))
        picked_stats_list.append(pick_stats(stats, 'evictions'))
        picked_stats_list.append(pick_stats(stats, 'cmd_flush'))
        picked_stats_list.append(pick_stats(stats, 'get_hits'))
        picked_stats_list.append(pick_stats(stats, 'get_misses'))
        picked_stats_list.append(pick_stats(stats, 'curr_connections'))
    
        print ' '.join(picked_stats_list)
#        '%s: EVI(%s), GET_MISS(%s)/GET_HIT(%s), FLUSH_TIME(%s), TOTAL_ITEM(%s) CURR_CONNECTION(%s)'%(s[0], s[1]['evictions'], s[1]['get_misses'], s[1]['get_hits'], s[1]['cmd_flush'], s[1]['total_items'], s[1]['curr_connections'])

def usage():
    filename = os.path.basename(__file__)
    print """
Usage: %s flush
       %s stats
"""%(filename, filename)

def main():
    if len(sys.argv) != 2:
        usage()
        return
    
    cache_settings = settings.APT_SERVICE_SETTINGS['aptcache']['connection']
    mc = memcache.Client(**cache_settings)
    func = {'flush': do_flush,
            'stats': do_stats,}
    try:
        func[sys.argv[1]](mc)
    except KeyError as e:
        usage()
        return

if __name__ == '__main__':   
    sys.exit(main())
