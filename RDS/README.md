AWS RDS Server Density plugin
=============================

This plugin allows to monitor AWS RDS instances. It is based on the [Percona Monitoring Tools](https://github.com/percona/percona-monitoring-plugins/blob/master/cacti/scripts/ss_get_rds_stats.py) and uses [Python Boto](http://boto.cloudhackers.com/en/latest/) to query AWS CloudWatch.

Every minute it pulls the 2 minute average from Cloudwatch and posts that to Server Density. The reason it pulls a 2 minute average rather than a 1 minute average is that when pulling a 1 minute average CPU utilization is not available.

In the configuration you can get data from multiple endpoints by adding instances. However, due to the nature of Boto making a request for each metric it's advisable to not have too many endpoints to allow the agent to make postbacks every minute.

Setup
-----

1. Configure the plugin in `/etc/sd-agent/conf.d/RDS.yaml`
```
init_config:

instances:
  - endpoint: "aws-endpoint"
    aws_secret_access_key: "your-secret--access-key"
    aws_access_key_id: "-your-access-key-id"
    #tags:         #OPTIONAL
    #  - your:tags
```
3. Drop the RDS.py script into the agent plugin directory at `/usr/share/python/sd-agent/checks.d/`.
4. Restart the agent to apply changes `sudo service sd-agent restart`

Troubleshooting
---------------

You can run the plugin individually with the agent with this command:

```
$ sudo -u sd-agent /usr/share/python/sd-agent/agent.py check rds
 {'hostname': 'scw-reverent-roentgen',
   'tags': ('i:tester', 'rds:database-1'),
   'type': 'gauge'}),
 ('rds.io.disk_queue_depth',
  1588772108,
  0.0,
  {'hostname': 'scw-reverent-roentgen',
   'tags': ('i:testee', 'rds:database-1'),
   'type': 'gauge'}),
 ('rds.db.connections',
  1588772108,
  0.0,
  {'hostname': 'scw-reverent-roentgen',
   'tags': ('i:testee', 'rds:database-1'),
   'type': 'gauge'}),
 ('rds.io.write_throughput',
  1588772108,
  0.00146774,
  {'hostname': 'scw-reverent-roentgen',
   'tags': ('i:testee', 'rds:database-1'),
   'type': 'gauge'}),
 ('rds.io.read_latency',
  1588772108,
  0.0,
  {'hostname': 'scw-reverent-roentgen',
   'tags': ('i:tester', 'rds:database-1'),
   'type': 'gauge'}),
 ('rds.io.write_throughput',
  1588772108,
  0.00146774,
  {'hostname': 'scw-reverent-roentgen',
   'tags': ('i:tester', 'rds:database-1'),
   'type': 'gauge'}),
 ('rds.io.write_iops',
  1588772108,
  0.14,
  {'hostname': 'scw-reverent-roentgen',
   'tags': ('i:tester', 'rds:database-1'),
   'type': 'gauge'}),
 ('rds.free_storage_space',
  1588772108,
  20068.175872,
  {'hostname': 'scw-reverent-roentgen',
   'tags': ('i:testee', 'rds:database-1'),
   'type': 'gauge'}),
 ('rds.free_storage_space',
  1588772108,
  20068.175872,
  {'hostname': 'scw-reverent-roentgen',
   'tags': ('i:tester', 'rds:database-1'),
   'type': 'gauge'}),
 ('rds.used_diskusage',
  1588772108,
  -68.1758719999998,
  {'hostname': 'scw-reverent-roentgen',
   'tags': ('i:tester', 'rds:database-1'),
   'type': 'gauge'}),
 ('rds.net.transmit_throughput',
  1588772108,
  0.0030705100000000003,
  {'hostname': 'scw-reverent-roentgen',
   'tags': ('i:tester', 'rds:database-1'),
   'type': 'gauge'}),
 ('rds.mem.freeable_memory',
  1588772108,
  489.97376,
  {'hostname': 'scw-reverent-roentgen',
   'tags': ('i:tester', 'rds:database-1'),
   'type': 'gauge'}),
 ('rds.bin_log_disk_usage',
  1588772108,
  0.0,
  {'hostname': 'scw-reverent-roentgen',
   'tags': ('i:tester', 'rds:database-1'),
   'type': 'gauge'}),
 ('rds.net.received_throughput',
  1588772108,
  0.00044559,
  {'hostname': 'scw-reverent-roentgen',
   'tags': ('i:testee', 'rds:database-1'),
   'type': 'gauge'}),
 ('rds.mem.used',
  1588772108,
  510.02624,
  {'hostname': 'scw-reverent-roentgen',
   'tags': ('i:tester', 'rds:database-1'),
   'type': 'gauge'}),
 ('rds.io.read_throughput',
  1588772108,
  0.0,
  {'hostname': 'scw-reverent-roentgen',
   'tags': ('i:testee', 'rds:database-1'),
   'type': 'gauge'}),
 ('rds.io.read_iops',
  1588772108,
  0.0,
  {'hostname': 'scw-reverent-roentgen',
   'tags': ('i:tester', 'rds:database-1'),
   'type': 'gauge'}),
 ('rds.net.received_throughput',
  1588772108,
  0.00044559,
  {'hostname': 'scw-reverent-roentgen',
   'tags': ('i:tester', 'rds:database-1'),
   'type': 'gauge'}),
 ('rds.io.read_iops',
  1588772108,
  0.0,
  {'hostname': 'scw-reverent-roentgen',
   'tags': ('i:testee', 'rds:database-1'),
   'type': 'gauge'}),
 ('rds.db.connections',
  1588772108,
  0.0,
  {'hostname': 'scw-reverent-roentgen',
   'tags': ('i:tester', 'rds:database-1'),
   'type': 'gauge'}),
 ('rds.io.disk_queue_depth',
  1588772108,
  0.0,
  {'hostname': 'scw-reverent-roentgen',
   'tags': ('i:tester', 'rds:database-1'),
   'type': 'gauge'})]
Events: 
[]
Service Checks: 
[]
Service Metadata: 
[{}, {}]
    rds
    -----------
      - instance #0 [OK]
      - instance #1 [OK]
      - Collected 36 metrics, 0 events & 0 service checks
  
```