"""
Server Density plugin
Foocast - Datacenter forecast monitoring

version: 0.1
"""

import sys
import logging
import json
import yaml
import time
import datetime

from geopy.geocoders import Nominatim
from forecastiopy import *


class Foocast(object):

    def __init__(self, agent_config, checks_logger, raw_config):

        self.agent_config = agent_config
        self.checks_logger = checks_logger
        self.raw_config = raw_config

        self.cfgfile = self.raw_config['Foocast'].get('cfg_file', 'datacenters.yaml')
        self.forecastio_key = self.raw_config['Foocast'].get('forecastio_key', '')
        self.run_interval = int(self.raw_config['Foocast'].get('run_interval', '3600'))
        self.geoloc = Nominatim()

        self.config = {}
        try:
            with open(self.cfgfile, 'r') as stream:
                try:
                    self.config = yaml.load(stream)
                except yaml.YAMLError as exception:
                    checks_logger.error('Failed to parse YAML configuration file: {0}'
                                        .format(exception.message))
        except Exception as exception:
            checks_logger.error('Failed to load configuration file: {0}'.format(exception.message))

    def fetch(self):

        data = {}
        for provider in self.config:
            for dc in self.config[provider]:
                location = self.config[provider][dc][0]['location']
                gdata = self.geoloc.geocode(location)
                fio = ForecastIO.ForecastIO(self.forecastio_key, latitude=gdata.latitude,
                                            longitude=gdata.longitude)

                if fio.has_daily() is True:
                    daily = FIODaily.FIODaily(fio)
                    precipIntensity = 0
                    windSpeed = 0
                    for day in xrange(0, daily.days()):
                        precipIntensity = max(precipIntensity,
                                              unicode(daily.get_day(day)['precipIntensity']))
                        windSpeed = max(windSpeed, unicode(daily.get_day(day)['windSpeed']))
                        name = provider + '_' + dc + '_precipIntensity'
                        data[name] = precipIntensity
                        name = provider + '_' + dc + '_windSpeed'
                        data[name] = windSpeed
        return data

    def run(self):

        time_path = '/tmp/foocast.time'
        json_path = '/tmp/foocast.json'

        now = int(time.time())
        lastrun = now

        try:
            with open(time_path, 'r+') as f:
                lastrun = int(f.read())
        except IOError:
            pass

        with open(time_path, 'w+') as f:
            f.write('{}'.format(now))

        next_run = lastrun + self.run_interval

        if now == lastrun:
            data = self.fetch()
            with open(json_path, 'w+') as data_file:
                json.dump(data, data_file)
        elif now > next_run:
            data = self.fetch()
            with open(json_path, 'w+') as data_file:
                json.dump(data, data_file)
        else:
            with open(json_path, 'r') as data_file:
                payload = data_file.read()
            data = json.loads(payload)
        return data


if __name__ == '__main__':
    """
    Standalone test configuration
    """
    raw_agent_config = {
        'Foocast': {
            'cfg_file': 'datacenters.yaml',
            'forecastio_key': '',
            'run_interval': 3600,
        }
    }

    main_checks_logger = logging.getLogger('Foocast')
    main_checks_logger.setLevel(logging.DEBUG)
    main_checks_logger.addHandler(logging.StreamHandler(sys.stdout))
    foocast = Foocast({}, main_checks_logger, raw_agent_config)

    while True:
        try:
            print json.dumps(foocast.run(), indent=4, sort_keys=True)
        except:
            main_checks_logger.exception("Unhandled exception")
        finally:
            time.sleep(60)
