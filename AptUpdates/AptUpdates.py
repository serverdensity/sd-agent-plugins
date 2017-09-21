import json
import sys
import subprocess
import logging
import time
import datetime



class AptUpdates(object):

    def __init__(self, agentConfig, checksLogger, rawConfig):
        self.agentConfig = agentConfig
        self.checksLogger = checksLogger
        self.rawConfig = rawConfig
        self.interval = int(self.rawConfig['AptUpdates'].get('CheckInterval','10')) * 60
        self.next_run_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=self.interval)
        self.data = {}

    def run(self):    
        if self.next_run_time < datetime.datetime.utcnow():
            apt_check = subprocess.check_output(
                    "/usr/lib/update-notifier/apt-check 2>&1", shell=True)
            updates,security = apt_check.split(';')

            self.data = {"updates": updates, "security": security, "check":1}
            self.next_run_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=self.interval)
            
            return self.data
        
        else:
            self.data['check'] = 0
            return self.data

if __name__ == '__main__':
    """
    Standalone test configuration
    """
    raw_agent_config = {
        'AptUpdates': {
            'CheckInterval': 2,
        }
    }

    main_checks_logger = logging.getLogger('AptUpdates')
    main_checks_logger.setLevel(logging.DEBUG)
    main_checks_logger.addHandler(logging.StreamHandler(sys.stdout))
    host_check = AptUpdates({}, main_checks_logger, raw_agent_config)

    while True:
        try:
            print json.dumps(host_check.run(), indent=4, sort_keys=True)
        except:
            main_checks_logger.exception("Unhandled exception")
        finally:
            time.sleep(60)