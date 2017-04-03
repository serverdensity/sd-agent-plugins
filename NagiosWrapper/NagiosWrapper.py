"""
Server Density plugin
NagiosWrapper
https://github.com/serverdensity/sd-agent-plugins/
version: 1.0
"""
import json
import subprocess

from crontab import CronTab


def str_to_bool(s):
    return s.lower() not in ('false', '0')


class NagiosWrapper:

    def __init__(self, agent_config, checks_logger, raw_config):
        self.agent_config = agent_config
        self.checks_logger = checks_logger
        self.raw_config = raw_config

    def run_check(self, data, plugins):
        get_extra_context = str_to_bool(
            self.raw_config.get('NagiosWrapper', {}).get('get_extra_context', 'False'))

        # subprocess needs a list containing the command and
        # its parameters
        plugins_list = plugins.split(" ")
        # the check command to retrieve it's name
        plugin_command = plugins_list[0]

        plugin_process = subprocess.Popen(
            plugins_list,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        out, err = plugin_process.communicate()

        self.checks_logger.debug(
            'Output of {0}: {1}'.format(plugin_command, out)
        )

        if err:
            self.checks_logger.error(
                'Error executing {0}: {1}'.format(plugin_command, err)
            )

        check_name = plugin_command.split("/")[-1]
        check_data = out.split("|")
        # the check command name = return value:
        # 0 - OK
        # 1 - WARNING
        # 2 - CRITICAL
        # 3 - UNKNOWN
        if get_extra_context:
            data[check_name] = {
                'value': plugin_process.returncode,
                'extra_context': check_data[0],
            }
        else:
            data[check_name] = plugin_process.returncode

        # add performance data if it exists
        if len(check_data) > 1:
            metric_data = check_data[1].split(";")[0].split("=")
            if get_extra_context:
                data[metric_data[0]] = {
                    'value': metric_data[1],
                    'extra_context': check_data[0],
                }
            else:
                data[metric_data[0]] = metric_data[1]

    def run(self):
        data = {}
        conf = json.loads(self.raw_config.get('NagiosWrapper', {}).get('commands', "{}"))
        for plugin in conf:
            cron_entry = CronTab(conf[plugin])
            if cron_entry.next() <= 60:
                self.run_check(data, plugin)
            else:
                self.checks_logger.debug("{0} run skipped".format(plugin))

        return data


if __name__ == '__main__':
    """Standalone test
    """

    import logging
    import sys
    import time

    raw_agent_config = {
        'NagiosWrapper': {
            'commands': """{
                "/usr/lib64/nagios/plugins/check_sensors": "* * * * *",
                "/usr/lib64/nagios/plugins/check_mailq -w 10 -c 20 -M postfix": "*/3 * * * *"
            }"""
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
