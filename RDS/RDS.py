"""
Server Density plugin
RDS monitoring script, based on
https://github.com/percona/percona-monitoring-plugins/blob/master/cacti/scripts/ss_get_rds_stats.py
version: 0.1
"""
import sys
import json
import time
import datetime
import boto
import boto.rds
import boto.ec2.cloudwatch
from boto.exception import BotoServerError
from checks import AgentCheck


class NoDBinstanceError(Exception):
    pass


class NoMetricError(Exception):
    pass


class BotoRDS(object):
    """RDS connection class"""
    def __init__(self, identifier, region, aws_key, aws_secret):
        """Get RDS instance details"""
        self.region = region
        self.identifier = identifier
        self.aws_key = aws_key
        self.aws_secret = aws_secret
        try:
            rds_conn = boto.rds.connect_to_region(
                self.region,
                aws_access_key_id=self.aws_key,
                aws_secret_access_key=self.aws_secret
            )
            self.info = rds_conn.get_all_dbinstances(self.identifier)[0]
        except IndexError:
            msg = 'No database instance found with identifier: {}'
            raise NoDBinstanceError(msg.format(identifier))

    def get_info(self):
        """Get RDS instance info"""
        return self.info

    def get_list(self):
        """Get list of available instances by region(s)"""
        result = dict()
        for reg in self.regions_list:
            try:
                rds = boto.rds.connect_to_region(
                    reg,
                    aws_access_key_id=self.aws_key,
                    aws_secret_access_key=self.aws_secret
                )
                result[reg] = rds.get_all_dbinstances()
            except (boto.provider.ProfileNotFoundError,
                    boto.exception.BotoServerError):
                result = {}
        return result

    def get_metric(self, metric):
        """Get RDS metric from CloudWatch"""
        cw_conn = boto.ec2.cloudwatch.connect_to_region(
            self.region,
            aws_access_key_id=self.aws_key,
            aws_secret_access_key=self.aws_secret
        )
        result = cw_conn.get_metric_statistics(
            120,  # period of time in seconds we want an average for
            datetime.datetime.utcnow() - datetime.timedelta(seconds=120),
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
        else:
            raise NoMetricError('There are no metric for {} in {}'.format(
                                metric, self.identifier))
        return float(result)


class RDS(AgentCheck):
    def preliminaries(self):
        self.config = {}
        try:
            aws_secret = self.instance.get('aws_secret_access_key', '')
            aws_key = self.instance.get('aws_access_key_id', '')
            self.config['aws_key'] = aws_key
            self.config['aws_secret'] = aws_secret
        except IndexError as e:
            self.log.exception(
                'RDS: Failed to read configuration file: {}'.format(e.message)
                )
            return False
        return True

    def get_identifier_region(self, endpoint):
        identifier, _, region, _, _, _ = endpoint.split('.')
        return identifier, region

    def fetch_stats(self, rds, tags):
        for metric, values in self.metrics.items():
            try:
                stats = rds.get_metric(metric)
                inst = rds.identifier
                if metric in self.byte_related:
                    # formatting to megabytes
                    stats = stats / 10**6
                if metric == 'FreeableMemory':
                    info = rds.get_info()
                    try:
                        memory = self.db_classes[info.instance_class] * 1000
                        used_mem = memory - stats
                        mem_name = self.metrics[metric]
                        self.gauge(
                            "rds.mem.used",
                            used_mem, tags + ["rds:{}".format(inst)]
                            )
                        self.gauge(
                            "rds.mem.total",
                            memory, tags + ["rds:{}".format(inst)]
                            )
                        self.gauge(
                            "rds.mem.{}".format(mem_name),
                            stats, tags + ["rds:{}".format(inst)]
                            )
                    except IndexError as e:
                        msg = 'RDS: Unknown DB instance class "{}"'
                        self.log.exception(msg.format(info.instance_class))
                elif metric == 'FreeStorageSpace':
                    info = rds.get_info()
                    storage = float(info.allocated_storage) * 1000
                    used = storage - stats
                    self.gauge(
                        self.metrics[metric],
                        stats, tags + ["rds:{}".format(inst)]
                        )
                    self.gauge(
                        "rds.used_diskusage",
                        used, tags + ["rds:{}".format(inst)]
                        )
                    self.gauge(
                        "rds.total_diskusage",
                        storage, tags + ["rds:{}".format(inst)]
                        )
                elif metric in self.byte_related:
                    self.gauge(
                        self.metrics[metric],
                        stats, tags + ["rds:{}".format(inst)]
                        )
                else:
                    self.gauge(
                        self.metrics[metric],
                        stats, tags + ["rds:{}".format(inst)]
                        )
            except NoMetricError as e:
                msg = 'RDS: {} was not available for {}'
                self.log.exception(msg.format(metric, rds.identifier))

    def check(self, instance):
        self.instance = instance
        # DB instance classes as listed on
        # http://docs.aws.amazon.com/
        # AmazonRDS/latest/UserGuide/Concepts.DBInstanceClass.html
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
        # RDS metrics http://docs.aws.amazon.com/
        # AmazonCloudWatch/latest/DeveloperGuide/rds-metricscollected.html
        self.metrics = {
            # The amount of disk space occupied by binary logs on the master.
            # Only on MySQL read replicas. Units: megabytes
            'BinLogDiskUsage': 'rds.bin_log_disk_usage',
            # The number of CPU credits that an instance has accumulated.
            # Only valid for T2 instances
            'CPUCreditBalance': 'rds.cpucredit.balance',
            # The number of CPU credits consumed during the specified period.
            # Only valid for T2 instances.
            'CPUCreditUsage': 'rds.cpucredit.usage',
            # The percentage of CPU utilization.  Units: Percent
            'CPUUtilization': 'rds.cpu.utilization',
            # The number of database connections in use.  Units: Count
            'DatabaseConnections': 'rds.db.connections',
            # The number of outstanding IOs (read/write requests) waiting
            # to access the disk.  Units: Count
            'DiskQueueDepth': 'rds.io.disk_queue_depth',
            # The amount of available storage space.  Units: megabytes
            'FreeStorageSpace': 'rds.free_storage_space',
            # The amount of available random access memory.  Units: megabytes
            'FreeableMemory': 'freeable_memory',
            'MaximumUsedTransactionIDs': 'maximum_used_transaction_ids',
            # The incoming (Receive) network traffic on the DB instance.
            # Units: megabytes/second
            'NetworkReceiveThroughput': 'rds.net.received_throughput',
            # The outgoing (Transmit) network traffic on the DB instance.
            # Units: megabytes/second
            'NetworkTransmitThroughput': 'rds.net.transmit_throughput',
            'OldestReplicationSlotLag': 'rds.oldest_replication_slot',
            # The average number of disk I/O operations per second.
            # Units: Count/Second
            'ReadIOPS': 'rds.io.read_iops',
            # The average amount of time taken per disk I/O operation.
            # Units: Seconds
            'ReadLatency': 'rds.io.read_latency',
            # The average number of megabytes read from disk per second.
            # Units: megabytes/Second
            'ReadThroughput': 'rds.io.read_throughput',
            # The amount of time a Read Replica DB Instance lags behind the
            # source DB Instance. Only on replicas. Units: Seconds
            'ReplicaLag': 'rds.replica_lag',
            # The amount of swap space used on the DB Instance.
            # Units: megabytes
            'SwapUsage': 'rds.swap_usage',
            'TransactionLogsDiskUsage': 'rds.transaction_logs_disk_usage',
            'TransactionLogsGeneration': 'rds.transaction_logs_generation',
            # The average number of disk I/O operations per second.
            # Units: Count/Second
            'WriteIOPS': 'rds.io.write_iops',
            # The average amount of time taken per disk I/O operation.
            # Units: Seconds
            'WriteLatency': 'rds.io.write_latency',
            # The average number of megabytes written to disk per second.
            # Units: megabytes/Second
            'WriteThroughput': 'rds.io.write_throughput'
        }
        self.byte_related = [
            'BinLogDiskUsage',
            'NetworkReceiveThroughput',
            'NetworkTransmitThroughput',
            'ReadThroughput',
            'SwapUsage',
            'WriteThroughput',
            'FreeableMemory',
            'FreeStorageSpace'
        ]
        if not self.preliminaries():
            return {}
        endpoint = self.instance.get('endpoint', '')
        tags = self.instance.get('tags', '')
        identifier, region = self.get_identifier_region(endpoint)
        try:
            rds = BotoRDS(identifier, region, **self.config)
        except NoDBinstanceError as e:
            self.log.exception('RDS: {}'.format(e.message))
        except BotoServerError as e:
            msg = 'Request invalid: {}'
            self.log.exception(msg.format(e.message))
        else:
            # mutable dictionary
            self.fetch_stats(rds, tags)
