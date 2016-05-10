"""
  Server Density Plugin
  Mdadm Check
  Version: 1.0.0
"""

import json
import logging
import platform
import sys
import subprocess
import time
import mdstat


class Mdadm(object):
    """ Check the "State" of the md disks using output from
        /proc/mdstat via mdstat https://pypi.python.org/pypi/mdstat/
    """

    def __init__(self, agent_config, checks_logger, raw_config):
        self.agent_config = agent_config
        self.checks_logger = checks_logger
        self.raw_config = raw_config
        self.version = platform.python_version_tuple()

    def run(self):
        output = {}
        try:
            data = mdstat.parse()
            for device in data['devices']:
                try:
                    status_dict = data['devices'][device]['status']
                except:
                    check_logger.error(
                        'Device %s status does not exist' % (device, ))
                    continue
                for key in status_dict.keys():
                    output['%s_%s' % (device, key)] = status_dict[key]
                if data['devices'][device]['status']['raid_disks'] !=\
                   data['devices'][device]['status']['non_degraded_disks']:
                    output[device + '_degraded'] = 'true'
                else:
                    output[device + '_degraded'] = 'false'
#                    To output each disk status as 'md0_sda_faulty'
#                    for disks in data['devices'][devices]['disks']:
#                        output[devices + '_' + disks + '_faulty'] = data['
#                            devices'][devices]['disks'][disks]['faulty']

        except OSError as exception:
            self.checks_logger.error(
                'Unable to find mdstat.'
                ' Error: {0}'.format(exception.message))
        return output


if __name__ == '__main__':
    """Standalone test
    """

    raw_agent_config = {
    }

    main_checks_logger = logging.getLogger('Mdadm')
    main_checks_logger.setLevel(logging.DEBUG)
    main_checks_logger.addHandler(logging.StreamHandler(sys.stdout))
    mdadm_check = Mdadm({}, main_checks_logger, raw_agent_config)

    while True:
        try:
            print json.dumps(mdadm_check.run(), indent=4, sort_keys="true")
        except:
            main_checks_logger.exception("Unhandled exception")
        finally:
            time.sleep(60)
