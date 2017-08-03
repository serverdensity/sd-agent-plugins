"""
  Server Density Plugin
  Network Interface monitor
  Version: 1.0.0
"""

import json
import logging
import platform
import sys
import subprocess
import time
import re


class NetworkInterface(object):
    """
    Check the "State" of the network interfaces using "ip link"
    """

    def __init__(self, agent_config, checks_logger, raw_config):
        self.agent_config = agent_config
        self.checks_logger = checks_logger
        self.raw_config = raw_config
        self.version = platform.python_version_tuple()

    def run(self):
        state_mapping = {
            'UP': 0,
            'DOWN': 1,
            'UNKNOWN': 2
        }

        data = {}

        try:
            proc = subprocess.Popen(
                ['ip', 'link'],
                stdout=subprocess.PIPE,
                close_fds=True)
            output = proc.communicate()[0]
        except Exception:
            e = sys.exc_info()[0]
            self.checks_logger.error('Network State Plugin Error: {0}'.format(e))
            data['check'] = 1
            return data
        for line in output.strip("\r\n").split("\n"):
            if line[0] and line[0].isdigit():
                interface = line.split(':', 2)[1].replace(' ', '')
                state = re.search('state(.*)mode', line)
                if interface != "lo":
                    if state.group(1).replace(' ', '') in state_mapping:
                        data[interface] = state_mapping.get(state.group(1).replace(' ', ''))
                    else:
                        data[interface] = 2
        data['check_status'] = 0
        return data


if __name__ == '__main__':
    """Standalone test
    """

    raw_agent_config = {
    }

    main_checks_logger = logging.getLogger('NetworkInterface')
    main_checks_logger.setLevel(logging.DEBUG)
    main_checks_logger.addHandler(logging.StreamHandler(sys.stdout))
    state_check = NetworkInterface({}, main_checks_logger, raw_agent_config)

    while True:
        try:
            print json.dumps(state_check.run(), indent=4, sort_keys=True)
        except:
            main_checks_logger.exception("Unhandled exception")
        finally:
            time.sleep(60)
