"""
Server Density plugin
RDS monitoring script, based on
https://github.com/percona/percona-monitoring-plugins/blob/master/cacti/scripts/ss_get_rds_stats.py

version: 0.1
"""

import sys
import logging
import json
import yaml
import time
import datetime

import boto
import boto.rds
import boto.ec2.cloudwatch


class BotoRDS(object):

    """RDS connection class"""

    def __init__(self, region, profile=None, identifier=None):
        """Get RDS instance details"""
        self.region = region
        self.profile = profile
        self.identifier = identifier

        if self.region == 'all':
            self.regions_list = [reg.name for reg in boto.rds.regions()]
        else:
            self.regions_list = [self.region]

        self.info = None
        if self.identifier:
            for reg in self.regions_list:
                try:
                    rds = boto.rds.connect_to_region(reg, profile_name=self.profile)
                    self.info = rds.get_all_dbinstances(self.identifier)
                except (boto.provider.ProfileNotFoundError, boto.exception.BotoServerError) as msg:
                    print 'msg'
                else:
                    # Exit on the first region and identifier match
                    self.region = reg
                    break

    def get_info(self):
        """Get RDS instance info"""
        if not self.info:
            print 'No DB instance "%s" found on your AWS account or %s region(s).' % (options.ident, options.region)
            sys.exit(1)

        return self.info[0]

    def get_list(self):
        """Get list of available instances by region(s)"""
        result = dict()
        for reg in self.regions_list:
            try:
                rds = boto.rds.connect_to_region(reg, profile_name=self.profile)
                result[reg] = rds.get_all_dbinstances()
            except (boto.provider.ProfileNotFoundError, boto.exception.BotoServerError) as msg:
                debug(msg)

        return result

    def get_metric(self, metric):
        """Get RDS metric from CloudWatch"""
        cw_conn = boto.ec2.cloudwatch.connect_to_region(self.region, profile_name=self.profile)
        result = cw_conn.get_metric_statistics(
            300,
            datetime.datetime.utcnow() - datetime.timedelta(seconds=300),
            datetime.datetime.utcnow(),
            metric,
            'AWS/RDS',
            'Average',
            dimensions={'DBInstanceIdentifier': [self.identifier]}
        )
        if result:
            if metric in ('ReadLatency', 'WriteLatency'):
                # Transform into miliseconds
                result = '%.2f' % float(result[0]['Average'] * 1000)
            else:
                result = '%.2f' % float(result[0]['Average'])

        elif metric == 'ReplicaLag':
            # This metric can be missed
            result = 0
        else:
            print 'Unable to get RDS statistics'
            sys.exit(1)

        return float(result)


class RDS(object):

    def __init__(self, agent_config, checks_logger, raw_config):
        self.agent_config = agent_config
        self.checks_logger = checks_logger
        self.raw_config = raw_config

        # DB instance classes as listed on
        # http://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.html
        self.db_classes = {
            'db.t1.micro': 0.615,
            'db.m1.small': 1.7,
            'db.m1.medium': 3.75,
            'db.m1.large': 7.5,
            'db.m1.xlarge': 15,
            'db.m4.large': 8,
            'db.m4.xlarge': 16,
            'db.m4.2xlarge': 32,
            'db.m4.4xlarge': 64,
            'db.m4.10xlarge': 160,
            'db.r3.large': 15,
            'db.r3.xlarge': 30.5,
            'db.r3.2xlarge': 61,
            'db.r3.4xlarge': 122,
            'db.r3.8xlarge': 244,
            'db.t2.micro': 1,
            'db.t2.small': 2,
            'db.t2.medium': 4,
            'db.t2.large': 8,
            'db.m3.medium': 3.75,
            'db.m3.large': 7.5,
            'db.m3.xlarge': 15,
            'db.m3.2xlarge': 30,
            'db.m2.xlarge': 17.1,
            'db.m2.2xlarge': 34.2,
            'db.m2.4xlarge': 68.4,
            'db.cr1.8xlarge': 244,
        }

        # RDS metrics http://docs.aws.amazon.com/AmazonCloudWatch/latest/DeveloperGuide/rds-metricscollected.html
        self.metrics = {
            'BinLogDiskUsage': 'binlog_disk_usage',  # The amount of disk space occupied by binary logs on the master.  Units: Bytes
            'CPUUtilization': 'utilization',  # The percentage of CPU utilization.  Units: Percent
            'DatabaseConnections': 'connections',  # The number of database connections in use.  Units: Count
            'DiskQueueDepth': 'disk_queue_depth',  # The number of outstanding IOs (read/write requests) waiting to access the disk.  Units: Count
            'ReplicaLag': 'replica_lag',  # The amount of time a Read Replica DB Instance lags behind the source DB Instance.  Units: Seconds
            'SwapUsage': 'swap_usage',  # The amount of swap space used on the DB Instance.  Units: Bytes
            'FreeableMemory': 'used_memory',  # The amount of available random access memory.  Units: Bytes
            'FreeStorageSpace': 'used_space',  # The amount of available storage space.  Units: Bytes
            'ReadIOPS': 'read_iops',  # The average number of disk I/O operations per second.  Units: Count/Second
            'WriteIOPS': 'write_iops',  # The average number of disk I/O operations per second.  Units: Count/Second
            'ReadLatency': 'read_latency',  # The average amount of time taken per disk I/O operation.  Units: Seconds
            'WriteLatency': 'write_latency',  # The average amount of time taken per disk I/O operation.  Units: Seconds
            'ReadThroughput': 'read_throughput',  # The average number of bytes read from disk per second.  Units: Bytes/Second
            'WriteThroughput': 'write_throughput',  # The average number of bytes written to disk per second.  Units: Bytes/Second
        }

        self.cfgfile = self.raw_config['RDS'].get('cfgfile', 'rds.yaml')

        self.config = {}
        try:
            with open(self.cfgfile, 'r') as stream:
                try:
                    self.config = yaml.load(stream)
                except yaml.YAMLError as exception:
                    checks_logger.error('Failed to parse YAML configuration file: {0}'.format(exception.message))
        except Exception as exception:
            checks_logger.error('Failed to load configuration file: {0}'.format(exception.message))

    def run(self):

        data = {}
        for profile in self.config:
            for region in self.config[profile]:
                for db in self.config[profile][region]:
                    if (profile == 'default'):
                        profile = None
                    rds = BotoRDS(region=region, profile=profile, identifier=db)
                    for metric in self.metrics.keys():

                        if metric == 'FreeableMemory':
                            info = rds.get_info()
                            try:
                                memory = self.db_classes[info.instance_class] * 1024 ** 3
                            except IndexError:
                                print 'Unknown DB instance class "%s"' % info.instance_class
                                sys.exit(1)
                            data['{0}_{1}_{2}'.format(
                                region, db, 'UsedMemory')] = memory - stats
                            data['{0}_{1}_{2}'.format(
                                region, db, 'TotalMemory')] = memory
                        elif metric == 'FreeStorageSpace':
                            info = rds.get_info()
                            storage = float(info.allocated_storage) * 1024 ** 3
                            data['{0}_{1}_{2}'.format(
                                region, db, 'UsedDiskUsage')] = storage - stats
                            data['{0}_{1}_{2}'.format(
                                region, db, 'TotalDiskUsage')] = storage
                        else:
                            stats = rds.get_metric(metric)
                            data['{0}_{1}_{2}'.format(
                                region, db, metric)] = stats

        return data

if __name__ == '__main__':
    """
    Standalone test configuration
    """
    raw_agent_config = {
        'RDS': {
            'cfg_file': 'rds.yaml',
        }
    }

    main_checks_logger = logging.getLogger('RDS')
    main_checks_logger.setLevel(logging.DEBUG)
    main_checks_logger.addHandler(logging.StreamHandler(sys.stdout))
    rds = RDS({}, main_checks_logger, raw_agent_config)

    while True:
        try:
            print json.dumps(rds.run(), indent=4, sort_keys=True)
        except:
            main_checks_logger.exception("Unhandled exception")
        finally:
            time.sleep(60)
