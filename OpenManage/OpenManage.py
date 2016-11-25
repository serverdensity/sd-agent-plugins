"""
  Server Density Plugin
  OpenManage RAID monitor
  Version: 1.0.0
"""

import json
import logging
import platform
import sys
import subprocess
import time


class OpenManage(object):
    """ Check the "State" of the pdisks using output from
        omreport storage pdisk controller=0
        and send back to Server Density for each pdisk. Also has a
        'check' status which indicates if the check completed
        successfully or not based on the number of disks in the
        response (configurable, see readme).
    """

    def __init__(self, agent_config, checks_logger, raw_config):
        self.agent_config = agent_config
        self.checks_logger = checks_logger
        self.raw_config = raw_config
        self.version = platform.python_version_tuple()

    def run(self):

        data = {}

        try:
            expected_disks = self.raw_config['OpenManage']['disk_count']
            self.checks_logger.debug('OpenManage config options found |' +
                                     ' Disk count: ' + str(expected_disks))
        except KeyError:
            self.checks_logger.debug(
                'OpenManage disk_count config option not found, using default')
            expected_disks = 2

        try:
            omreport_location = self.raw_config['OpenManage']['om_report']
            self.checks_logger.debug('OpenManage config options found |' +
                                     ' Location: ' + omreport_location)
        except KeyError:
            self.checks_logger.debug(
                'OpenManage om_report config option not found, using default')
            omreport_location = '/opt/dell/srvadmin/bin/omreport'

        try:
            proc = subprocess.Popen(
                [omreport_location, 'storage', 'pdisk', 'controller=0'],
                stdout=subprocess.PIPE,
                close_fds=True)
            output = proc.communicate()[0]
        except Exception:
            e = sys.exc_info()[0]
            self.checks_logger.error('OpenManage Plugin Error: {0}'.format(e))
            data['check'] = 1
            return data
        for line in output.split("\n"):
            if line.startswith('ID'):
                ID = line.split(':', 1)[1].replace(' ', '')
            if line.startswith('State'):
                state = line.split(':')[1].replace(' ', '')
                if state != 'Online':
                    state = 1
                else:
                    state = 0
                data['state' + str(ID)] = state
        if len(data) >= int(expected_disks):
            data['check'] = 0
        else:
            data['check'] = 1
        return data


if __name__ == '__main__':
    """Standalone test
    """

    raw_agent_config = {
    }

    main_checks_logger = logging.getLogger('OpenManage')
    main_checks_logger.setLevel(logging.DEBUG)
    main_checks_logger.addHandler(logging.StreamHandler(sys.stdout))
    om_check = OpenManage({}, main_checks_logger, raw_agent_config)

    while True:
        try:
            print json.dumps(om_check.run(), indent=4, sort_keys=True)
        except:
            main_checks_logger.exception("Unhandled exception")
        finally:
            time.sleep(60)
