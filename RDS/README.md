AWS RDS Server Density plugin
=============================

This plugin allows to monitor AWS RDS instances. It is based on the [Percona Monitoring Tools](https://github.com/percona/percona-monitoring-plugins/blob/master/cacti/scripts/ss_get_rds_stats.py) and uses [Python Boto](http://boto.cloudhackers.com/en/latest/) to query AWS CloudWatch.

Every minute it pulls the 2 minute average from Cloudwatch and posts that to Server Density. The reason it pulls a 2 minute average rather than a 1 minute average is that when pulling a 1 minute average CPU utilization is not available.

In the configuration you can get data from multiple endpoints by separating the endpoints through a comma. However, due to the nature of Boto making a request for each metric it's advisable to not have too many endpoints to allow the agent to make postbacks every minute.

Setup
-----

1. Install python-boto `sudo apt-get install python-boto`
2. Configure the plugin in `/etc/sd-agent/plugins.cfg`
```
[RDS]
aws_access_key_id = YOUR_KEY_ID
aws_secret_access_key = YOUR_ACCESS_KEY
endpoints = RDS_ENDPOINT1,RDS_ENDPOINT2
```

3. Drop the RDS.py script in your plugin directory, most likely `/usr/local/share/sd-plugins/`. Check your `config.cfg` if you're unsure.
4. Restart the agent to apply changes `sudo service sd-agent restart`

Troubleshooting
---------------

You can run the script directly from the command line to collect the metrics:

```
$ python RDS.py -k YOUR_ACCESS_KEY -p YOUR_SECRET -e YOUR_ENDPOINT
{
  "somedbinstance_total_diskUsage": 5368709120.0,
  "somedbinstance_database_connections": 0.0,
  "somedbinstance_used_memory": 466810880.0,
  "somedbinstance_free_storage_space": 4446867456.0,
  "somedbinstance_network_transmit_throughput": 2634.76,
  "somedbinstance_write_latency": 0.41,
  "somedbinstance_read_latency": 0.2,
  "somedbinstance_cpuutilization": 1.33,
  "somedbinstance_maximum_used_transaction_ids": 616.0,
  "somedbinstance_read_iops": 0.55,
  "somedbinstance_write_throughput": 8328.87,
  "somedbinstance_somedbinstance": 606930944.0,
  "somedbinstance_oldest_replication_slot": -1.0,
  "somedbinstance_network_received_throughput": 178.44,
  "somedbinstance_write_iops": 0.78,
  "somedbinstance_disk_queue_depth": 0.0,
  "somedbinstance_transaction_logs_disk_usage": 570433832.0,
  "somedbinstance_transaction_logs_generation": 0.0,
  "somedbinstance_used_diskusage": 921841664.0,
  "somedbinstance_total_memory": 1073741824,
  "somedbinstance_read_throughput": 341.32,
  "somedbinstance_swap_usage": 28672.0
}
```

Additional Notes
----------------

This plugin requires at least python-boto 2.35.2, Ubuntu 14.04 can use [Chris Lea's PPA](https://launchpad.net/~chris-lea/+archive/ubuntu/python-boto).