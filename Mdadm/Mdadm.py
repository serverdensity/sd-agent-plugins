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
    """ Check the "State" of the controller using output from
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
            for devices in data['devices']:
                for device in data['devices'][devices]:
                    try:
                        output[devices + '_raid_disks'] = data['devices'][devices]['status']['raid_disks']
                    except KeyError:
                        pass
                    try:    
                        output[devices + '_non_degraded_disks'] = data['devices'][devices]['status']['non_degraded_disks']
                    except KeyError:
                        pass                        
                    try:
                        output[devices + '_near_copies'] = data['devices'][devices]['status']['near_copies']
                    except KeyError:
                        pass                        
                    try:                       
                        output[devices + '_blocks'] = data['devices'][devices]['status']['blocks']
                    except KeyError:
                        pass                        
                    try:
                        output[devices + '_offset_copies'] = data['devices'][devices]['status']['offset_copies']
                    except KeyError:
                        pass                        
                    try:
                        output[devices + '_sync_request'] = data['devices'][devices]['status']['sync_request']
                    except KeyError:
                        pass                        
                    try:
                        output[devices + '_far_copies'] = data['devices'][devices]['status']['far_copies']
                    except KeyError:
                        pass                        
                    try:
                        output[devices + '_synced'] = data['devices'][devices]['status']['synced']
                    except KeyError:
                        pass                        
                    try:
                        output[devices + '_chunks'] = data['devices'][devices]['status']['chunks']
                    except KeyError:
                        pass                        
                    try:
                        output[devices + '_super'] = data['devices'][devices]['status']['super']
                    except KeyError:
                        pass                                    
                    if data['devices'][devices]['status']['raid_disks'] != data['devices'][devices]['status']['non_degraded_disks']:
                        output[devices + '_degraded'] = 'true'
                    else:
                        output[devices + '_degraded'] = 'false'
                    #To output each disk status as 'md0_sda_faulty' 
                    #for disks in data['devices'][devices]['disks']:
                        #output[devices + '_' + disks + '_faulty'] = data['devices'][devices]['disks'][disks]['faulty'] 
        
        except OSError as exception:
            self.checks_logger.error(
                'Unable to find mdstat.'
                ' Error: {0}'.format(exception.message))
        except KeyError:
            pass
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