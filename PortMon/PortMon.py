#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import socket


class PortMon(object):
    '''
    Config should be in /etc/sd-agent/plugins.cfg like:

    [PortMon]
    portmon_timeout: 5
    portmon_targets: 127.0.0.1:22,192.168.3.4:5678

    Multiple targets to be monitored should be separated with a ','.
    '''

    def __init__(self, agentConfig, checksLogger, rawConfig):
        self.agentConfig = agentConfig
        self.checksLogger = checksLogger
        self.rawConfig = rawConfig

        self.timeout = int(rawConfig['PortMon'].get('portmon_timeout', 10))
        targets_str = rawConfig['PortMon'].get('portmon_targets', '').strip()
        if len(targets_str):
            self.targets = targets_str.split(',')
        else:
            self.targets = []

    def run(self):
        target_times = {}
        for t in self.targets:
            host, port = t.split(':')
            key = t.replace('.', '_')
            target_times[key] = self.timeConnect(host, int(port))
        return target_times

    def timeConnect(self, host, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(self.timeout)
        t_init = time.time()
        # ret = None
        try:
            s.connect((host, port))
            ret = time.time() - t_init
            # s.recv(0)
            s.close()
        except (socket.error, socket.timeout):
            return 'down'
        return ret

if __name__ == "__main__":

    # Test ports: one that's not accessible and another that's open on my
    # MacBook.
    fake_rawConfig = {
        'PortMon': {
            'portmon_targets': "127.0.0.1:8542,192.168.6.6:1200",
            'portmon_timeout': "10"
        }
    }
    pm = PortMon({}, {}, fake_rawConfig)
    print pm.run()
