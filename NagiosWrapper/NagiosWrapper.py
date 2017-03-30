import subprocess
import datetime
import logging
import sys
import time
import json

class NagiosWrapper:
    def __init__(self, agent_config, checks_logger, raw_config):
        self.agent_config = agent_config
        self.checks_logger = checks_logger
        self.raw_config = raw_config
        self.next_execution = {}
        self.data = {}

    def run_check(self, pluginCommandLine):
        # subprocess needs a list containing the command and
        # its parameters
        pluginCommandLineList = pluginCommandLine.split(" ")
        # the check command to retrieve it's name
        pluginCommand = pluginCommandLineList[0]

        p = subprocess.Popen(
            pluginCommandLineList,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        out, err = p.communicate()

        self.checks_logger.debug(
            'Output of {0}: {1}'.format(pluginCommand, out)
        )

        if err:
            self.checks_logger.error(
                'Error executing {0}: {1}'.format(pluginCommand, err)
            )

        # the check command name = return value:
        # 0 - OK
        # 1 - WARNING
        # 2 - CRITICAL
        # 3 - UNKNOWN
        self.data[pluginCommand.split("/")[-1]] = p.returncode

        # add performance data if it exists
        perfData = out.split("|")
        if len(perfData) > 1:
            self.data[perfData[1].split(";")[0].split("=")[0]] = perfData[
                1].split(";")[0].split("=")[1]


    def run(self):
        now = time.time()
        self.data = {}
        conf = json.loads(self.raw_config.get('NagiosWrapper', {}).get('commands', {}))
        for pluginCommandLine in conf:
            if pluginCommandLine not in self.next_execution:
                self.next_execution[pluginCommandLine] = now + (conf[pluginCommandLine] * 60)
                self.run_check(pluginCommandLine)
            if self.next_execution[pluginCommandLine] < now:
                self.run_check(pluginCommandLine)
                self.next_execution[pluginCommandLine] =  now + (conf[pluginCommandLine] * 60)
        return self.data

if __name__ == '__main__':
    """Standalone test
    """

    raw_agent_config = {
    'NagiosWrapper' :{
        'nagiosPluginsCommandLines' : {
        "/usr/lib64/nagios/plugins/check_sensors" : 1,
        "/usr/lib64/nagios/plugins/check_mailq -w 10 -c 20 -M postfix" : 3,
        }
    }
    }

    main_checks_logger = logging.getLogger('NagiosWrapper')
    main_checks_logger.setLevel(logging.DEBUG)
    main_checks_logger.addHandler(logging.StreamHandler(sys.stdout))
    check = NagiosWrapper({}, main_checks_logger, raw_agent_config)

    while True:
        try:
            print json.dumps(check.run(), indent=4, sort_keys=True)
        except:
            main_checks_logger.exception("Unhandled exception")
        finally:
            time.sleep(60)
