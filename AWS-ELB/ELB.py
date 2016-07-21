import json
import time
import logging
import sys
import datetime

import boto
import boto.ec2.elb
import boto.ec2.cloudwatch
from boto.exception import BotoServerError


class NoDBinstanceError(Exception):
    pass


class NoMetricError(Exception):
    pass


class BotoELB(object):

    """ELB connection class"""

    def __init__(self, identifier, region, aws_key, aws_secret):
        """Get ELB instance details"""
        self.region = region
        self.identifier = identifier
        self.aws_key = aws_key
        self.aws_secret = aws_secret

        try:
            elb_conn = boto.ec2.elb.connect_to_region(
                self.region,
                aws_access_key_id=self.aws_key,
                aws_secret_access_key=self.aws_secret
            )
            elb_conn.get_all_load_balancers(load_balancer_names=[self.identifier])[0]
        except IndexError:
            msg = 'No loadbalancer found with identifier: {}'
            raise NoDBinstanceError(msg.format(identifier))

    def get_metric(self, metric):
        """Get ELB metric from CloudWatch"""
        cw_conn = boto.ec2.cloudwatch.connect_to_region(
            self.region,
            aws_access_key_id=self.aws_key,
            aws_secret_access_key=self.aws_secret
        )
        funcd = {
            'HealthyHostCount': 'Average',
            'UnHealthyHostCount': 'Average',
            'Latency': 'Average',
            'SurgeQueueLength': 'Maximum'
        }
        func = funcd.get(metric, 'Sum')

        result = cw_conn.get_metric_statistics(
            60,  # period of time in seconds we want an average for
            datetime.datetime.utcnow() - datetime.timedelta(seconds=60),
            datetime.datetime.utcnow(),
            metric,
            'AWS/ELB',
            func,
            dimensions={'LoadBalancerName': [self.identifier]}
        )
        # fix me unneeded
        if result:
            if metric in ('Latency'):
                # Transform into miliseconds
                result = '%.2f' % float(result[0][func] * 1000)
            else:
                result = '%.2f' % float(result[0][func])
        else:
            # No metric provided by cloudwatch
            result = 0
        return float(result)


class ELB(object):

    def __init__(self, agent_config, checks_logger, raw_config):
        self.agent_config = agent_config
        self.checks_logger = checks_logger
        self.raw_config = raw_config

        # more info on metrics
        # http://docs.aws.amazon.com/ElasticLoadBalancing
        # /latest/DeveloperGuide/elb-cloudwatch-metrics.html
        self.metrics = {
            'HealthyHostCount': 'healthy_host_count',
            'UnHealthyHostCount': 'unhealthy_host_count',
            'RequestCount': 'request_count',
            'Latency': 'latency',
            'SurgeQueueLength': 'surge_queue_length',
            'SpilloverCount': 'spillover_count',
            'HTTPCode_ELB_4XX': 'http_code_elb_4xx',
            'HTTPCode_ELB_5XX': 'http_code_elb_5xx',
            'HTTPCode_Backend_2XX': 'http_code_backend_2xx',
            'HTTPCode_Backend_3XX': 'http_code_backend_3xx',
            'HTTPCode_Backend_4XX': 'http_code_backend_4xx',
            'HTTPCode_Backend_5XX': 'http_code_backend_5xx',
            'BackendConnectionErrors': 'backend_connection_errors',
        }

    def preliminaries(self):
        self.config = {}
        try:
            aws_secret = self.raw_config['ELB']['aws_secret_access_key']
            aws_key = self.raw_config['ELB']['aws_access_key_id']

            self.config['aws_key'] = aws_key
            self.config['aws_secret'] = aws_secret
        except IndexError as e:
            self.checks_logger.error(
                'ELB: Failed to read configuration file: {}'.format(e.message))
            return False
        return True

    def get_identifier_region(self, endpoint):
        identifier, region = endpoint.split(':')
        return identifier, region

    def fetch_stats(self, data, elb):
        for metric, values in self.metrics.items():
            try:
                stats = elb.get_metric(metric)
                inst = elb.identifier
                data['{0}_{1}'.format(inst, self.metrics[metric])] = stats
            except NoMetricError as e:
                msg = 'ELB: {} was not available for {}'
                self.checks_logger.info(msg.format(metric, elb.identifier))

    def run(self):
        if not self.preliminaries():
            return {}

        data = {}

        endpoints = self.raw_config['ELB']['elb_identifier_region']
        endpoints = endpoints.split(',')
        for endpoint in endpoints:
            identifier, region = self.get_identifier_region(endpoint)
            try:
                elb = BotoELB(identifier, region, **self.config)
            except NoDBinstanceError as e:
                self.checks_logger.error('ELB: {}'.format(e.message))
            except BotoServerError as e:
                msg = 'Request invalid: {}'
                self.checks_logger.exception(msg.format(e.message))
            else:
                # mutable dictionary
                self.fetch_stats(data, elb)

        return data

if __name__ == '__main__':
    """
    Standalone test configuration
    """
    import argparse

    parser = argparse.ArgumentParser(description='Configuration input')
    parser.add_argument('-k', dest='key', help='AWS access key')
    parser.add_argument('-p', dest='passw', help='AWS secret access key')
    parser.add_argument('-e', dest='elb_identifier_region', help='Endpoint for database')
    args = parser.parse_args()

    raw_agent_config = {
        'ELB': {
            'aws_access_key_id': args.key,
            'aws_secret_access_key': args.passw,
            'elb_identifier_region': args.elb_identifier_region
        }
    }

    main_checks_logger = logging.getLogger('ELB')
    main_checks_logger.setLevel(logging.DEBUG)
    main_checks_logger.addHandler(logging.StreamHandler(sys.stdout))
    rds = ELB({}, main_checks_logger, raw_agent_config)

    while True:
        try:
            print json.dumps(rds.run(), indent=4, sort_keys=True)
        except:
            main_checks_logger.exception("Unhandled exception")
        finally:
            time.sleep(60)
