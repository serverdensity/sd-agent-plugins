from multiprocessing.dummy import Pool
from subprocess import Popen, PIPE


class RunningProcesses:
    def __init__(self, agentConfig, logger, rawConfig):
        self.agentConfig = agentConfig
        self.logger = logger
        self.rawConfig = rawConfig
        self.data = {}

    def extractResult(self, process):
        errorOutput = process.communicate()[1]
        returnCode = process.returncode

        if (returnCode > 1):
            self.logger.error(
                'Error detecting status of {0}: {1}'.format(
                    process.name, error))

        self.data[process.name] = 1 if (returnCode == 0) else 0

    def run(self):
        if 'Running Processes' not in self.rawConfig:
            self.logger.warning(
                    'Could not find Running Processes section in config')
            return {}

        if 'process_list' not in self.rawConfig['Running Processes']:
            self.logger.warning('Could not find list of processes to watch')
            return {}

        processes = []
        processNames = self.rawConfig['Running Processes']['process_list']

        for processName in processNames.split(','):
            p = Popen(['pgrep', processName], stderr=PIPE)
            p.name = processName
            processes.append(p)

        Pool(len(processes)).map(self.extractResult, processes)

        return self.data
