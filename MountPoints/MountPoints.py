"""
  Server Density Plugin
  Mount Point Check
  Version: 1.0.0
"""

import json
import logging
import platform
import sys
import subprocess
import time


class MountPoints(object):
    """
    List all of the mount points in a string and return them to Server Density.
    Create 'does not contain' alerts for the mounts you wish to monitor.
    """
    def __init__(self, agent_config, checks_logger, raw_config):
        self.agent_config = agent_config
        self.checks_logger = checks_logger
        self.raw_config = raw_config
        self.version = platform.python_version_tuple()

    def run(self):
        data = {}

        p = subprocess.Popen(
            ['df', '-T'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        output, errorOutput = p.communicate()

        self.checks_logger.debug(
            'df -T command output: {0}'.format(output)
        )

        if errorOutput:
            self.checks_logger.error(
                'Error executing df -T {0}'.format(output))

        all_devices = [l.strip().split() for l in output.splitlines()]

        # Skip the header row and empty lines.
        raw_devices = [l for l in all_devices[1:] if l]

        mountedlist = []
        for child in raw_devices:
            mountedlist.append(child[6])

        data['mounted'] = ','.join(mountedlist)
        return data

if __name__ == '__main__':
    """Standalone test
    """

    raw_agent_config = {
    }

    main_checks_logger = logging.getLogger('MountPoints')
    main_checks_logger.setLevel(logging.DEBUG)
    main_checks_logger.addHandler(logging.StreamHandler(sys.stdout))
    mount_check = MountPoints({}, main_checks_logger, raw_agent_config)

    while True:
        try:
            print json.dumps(mount_check.run(), indent=4, sort_keys=True)
        except:
            main_checks_logger.exception("Unhandled exception")
        finally:
            time.sleep(60)
