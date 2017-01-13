"""
Server Density Nagios plugin
"""

import sys
import re
import logging
import json
import time
import subprocess

METRICS = [
    'Total Services',
    'Services Checked',
    'Services Scheduled',
    'Services Actively Checked',
    'Services Passively Checked',
    'Services Flapping',
    'Services In Downtime',
    'Total Hosts',
    'Hosts Checked',
    'Hosts Scheduled',
    'Hosts Actively Checked',
    'Host Passively Checked',
    'Hosts Flapping',
    'Hosts In Downtime'
]

METRICS_3AVG = [
    'Passive Host Checks Last 1/5/15 min',
    'Passive Service Checks Last 1/5/15 min',
    'External Commands Last 1/5/15 min'
]

METRICS_3AVGf = [
    'Total Service State Change',
    'Active Service Latency',
    'Active Service Execution Time',
    'Active Service State Change',
    'Passive Service Latency',
    'Passive Service State Change',
    'Total Host State Change',
    'Active Host Latency',
    'Active Host Execution Time',
    'Active Host State Change',
    'Passive Host Latency',
    'Passive Host State Change'
]

METRICS_4AVG = [
    'Active Services Last 1/5/15/60 min',
    'Passive Services Last 1/5/15/60 min',
    'Active Hosts Last 1/5/15/60 min',
    'Passive Hosts Last 1/5/15/60 min'
]


class Nagios:

    def __init__(self, agent_config, checks_logger, raw_config):
        self.agent_config = agent_config
        self.checks_logger = checks_logger
        self.raw_config = raw_config
        self.datastore = {}

        self.cmd_path = self.raw_config['Nagios'].get('cmd_path',
                                                      '/usr/local/nagios/bin/nagiostats')

    def run(self):
        data = ''
        stats = {}

        try:
            data = subprocess.check_output([self.cmd_path])
        except Exception as e:
            self.checks_logger.error('Failed to run %s: %s' % (self.cmd_path, e))
            return stats

        for metric in METRICS:
            stats[metric] = int(re.search("{0}:\s+(\d+)".format(metric), data).group(1))

        for metric in METRICS_3AVG:
            m = re.search("{0}:\s+(\d+)\s+/\s+(\d+)\s+/\s+(\d+)".format(metric), data)
            metric_name = re.match(r"(.*) Last 1/5/15 min", metric).group(1)
            stats[metric_name] = int(m.group(1))

        for metric in METRICS_3AVGf:
            m = re.search("{0}:\s+(\d+\.\d+)\s+/\s+(\d+\.\d+)\s+/\s+(\d+\.\d+)".format(metric),
                          data)
            stats[metric] = float(m.group(1))

        for metric in METRICS_4AVG:
            m = re.search("{0}:\s+(\d+)\s+/\s+(\d+)\s+/\s+(\d+)\s+/\s+(\d+)".format(metric), data)
            metric_name = re.match(r"(.*) Last 1/5/15/60 min", metric).group(1)
            stats[metric_name] = int(m.group(1))

        m = re.search("Services Ok/Warn/Unk/Crit:\s+(\d+)\s+/\s+(\d+)\s+/\s+(\d+)\s+/\s+(\d+)"
                      .format(metric), data)
        stats['Services Status Ok'] = int(m.group(1))
        stats['Services Status Warn'] = int(m.group(2))
        stats['Services Status Unknown'] = int(m.group(3))
        stats['Services Status Critical'] = int(m.group(4))

        m = re.search("Hosts Up/Down/Unreach:\s+(\d+)\s+/\s+(\d+)\s+/\s+(\d+)".format(metric), data)
        stats['Hosts Status Up'] = int(m.group(1))
        stats['Hosts Status Down'] = int(m.group(2))
        stats['Hosts Status Unreachable'] = int(m.group(3))

        m = re.search("Active Host Checks Last 1/5/15 min:\s+(\d+)\s+/\s+(\d+)\s+/\s+(\d+)\s+"
                      "Scheduled:\s+(\d+)\s+/\s+(\d+)\s+/\s+(\d+)\s+"
                      "On-demand:\s+(\d+)\s+/\s+(\d+)\s+/\s+(\d+)\s+"
                      "Parallel:\s+(\d+)\s+/\s+(\d+)\s+/\s+(\d+)\s+"
                      "Serial:\s+(\d+)\s+/\s+(\d+)\s+/\s+(\d+)\s+"
                      "Cached:\s+(\d+)\s+/\s+(\d+)\s+/\s+(\d+)\s+", data)
        stats['Active Host Checks Total'] = int(m.group(1))
        stats['Active Host Checks Scheduled'] = int(m.group(4))
        stats['Active Host Checks On-demand'] = int(m.group(7))
        stats['Active Host Checks Parallel'] = int(m.group(10))
        stats['Active Host Checks Serial'] = int(m.group(13))
        stats['Active Host Checks Cached'] = int(m.group(16))

        m = re.search("Active Service Checks Last 1/5/15 min:\s+(\d+)\s+/\s+(\d+)\s+/\s+(\d+)\s+"
                      "Scheduled:\s+(\d+)\s+/\s+(\d+)\s+/\s+(\d+)\s+"
                      "On-demand:\s+(\d+)\s+/\s+(\d+)\s+/\s+(\d+)\s+"
                      "Cached:\s+(\d+)\s+/\s+(\d+)\s+/\s+(\d+)\s+", data)
        stats['Active Service Checks Total'] = int(m.group(1))
        stats['Active Service Checks Scheduled'] = int(m.group(4))
        stats['Active Service Checks On-demand'] = int(m.group(7))
        stats['Active Service Checks Cached'] = int(m.group(10))

        m = re.search("Program Running Time:\s+(\d+)d\s+(\d+)h\s+(\d+)m\s+(\d+)s".format(metric),
                      data)
        stats['Uptime'] = (
            int(m.group(4)) +
            int(m.group(3)) * 60 +
            int(m.group(3)) * 3600 +
            int(m.group(4)) * 86400)

        return stats


if __name__ == '__main__':
    """
    Standalone test configuration
    """
    raw_agent_config = {
        'Nagios': {
            'cmd_path': '/usr/local/nagios/bin/nagiostats',
        }
    }

    main_checks_logger = logging.getLogger('Nagios')
    main_checks_logger.setLevel(logging.DEBUG)
    main_checks_logger.addHandler(logging.StreamHandler(sys.stdout))
    host_check = Nagios({}, main_checks_logger, raw_agent_config)

    while True:
        try:
            print json.dumps(host_check.run(), indent=4, sort_keys=True)
        except:
            main_checks_logger.exception("Unhandled exception")
        finally:
            time.sleep(60)
