"""
Server Density Nagios plugin
requires Icinga API feature enabled, see:
http://docs.icinga.org/icinga2/latest/doc/module/icinga2/chapter/icinga2-api
"""

import sys
import re
import logging
import json
import time
import requests


class Icinga:

    def __init__(self, agent_config, checks_logger, raw_config):
        self.agent_config = agent_config
        self.checks_logger = checks_logger
        self.raw_config = raw_config
        self.datastore = {}

        self.api_user = self.raw_config['Icinga'].get('api_user', 'root')
        self.api_passwd = self.raw_config['Icinga'].get('api_passwd', '')
        self.api_status_url = self.raw_config['Icinga'].get('api_stats_url',
                                                            'https://localhost:5665/v1/status')
        self.icinga_ca_crt = self.raw_config['Icinga'].get('icinga_ca_crt',
                                                           '/etc/icinga2/pki/ca.crt')

    def run(self):
        data = ''
        stats = {}

        try:
            r = requests.get(self.api_status_url,
                             auth=(self.api_user, self.api_passwd),
                             verify=self.icinga_ca_crt,)

            if (r.status_code == 200):
                data = r.json()
            else:
                r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            self.checks_logger.error('Failed to retrieve URL: %s' % (e, ))
            return stats

        cib_status = filter(lambda result: result['name'] == 'CIB', data['results'])
        stats = cib_status[0]['status']

        return stats


if __name__ == '__main__':
    """
    Standalone test configuration
    """
    raw_agent_config = {
        'Icinga': {
            'api_user': 'root',
            'api_passwd': '',
            'api_stats_url': 'http://localhost:5665/v1/status',
        }
    }

    main_checks_logger = logging.getLogger('Icinga')
    main_checks_logger.setLevel(logging.DEBUG)
    main_checks_logger.addHandler(logging.StreamHandler(sys.stdout))
    host_check = Icinga({}, main_checks_logger, raw_agent_config)

    while True:
        try:
            print json.dumps(host_check.run(), indent=4, sort_keys=True)
        except:
            main_checks_logger.exception("Unhandled exception")
        finally:
            time.sleep(60)
