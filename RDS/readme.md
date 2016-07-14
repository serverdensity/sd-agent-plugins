AWS RDS Server Density plugin
=============================

This plugin allows to monitor AWS RDS instances. It is based on the [Percona Monitoring Tools](https://github.com/percona/percona-monitoring-plugins/blob/master/cacti/scripts/ss_get_rds_stats.py) and uses [Python Boto](http://boto.cloudhackers.com/en/latest/) to query AWS CloudWatch.

Setup
-----

1. Install python-boto `sudo apt-get install python-boto`
2. Configure your [boto credentials](http://boto.cloudhackers.com/en/latest/boto_config_tut.html):
   for this SD plugin need to create /etc/boto.cfg with the following contents:

     ```
     [Credentials]
      aws_access_key_id = YOUR_KEY_ID
      aws_secret_access_key = YOUR_ACCESS_KEY
     ```
    And give it secure permisions: `sudo chown sd-agent:sd-agent /etc/boto.cfg ; sudo chmod 0640 /etc/boto.cfg`
3. Drop the RDS.py script in your plugin directory, most likely `/usr/local/share/sd-plugins/`
4. Configure the plugin YAML file, for example in `/etc/sd-agent/conf.d/rds.yaml`:

    ```
    ---
    default:
      eu-west-1:
        - my_monitored_rds_instance
        - another_monitored_rds_instnace
    ```
5. Configure the plugin, in `/etc/sd-agent/plugins.cfg`:

    ```
    [RDS]
    cfgfile = /etc/sd-agent/conf.d/rds.yaml
    ```
6. Restart the agent to apply changes `sudo service sd-agent restart`

Troubleshooting
---------------

You can run the script directly from the command line to collect the metrics:

```
$ python RDS.py         
{
    "eu-west-1_sddb_BinLogDiskUsage": 817.8, 
    "eu-west-1_sddb_CPUUtilization": 18.31, 
    "eu-west-1_sddb_DatabaseConnections": 0.0, 
    "eu-west-1_sddb_DiskQueueDepth": 0.0, 
    "eu-west-1_sddb_ReadIOPS": 0.22, 
    "eu-west-1_sddb_ReadLatency": 0.08, 
    "eu-west-1_sddb_ReadThroughput": 136.54, 
    "eu-west-1_sddb_ReplicaLag": 0.0, 
    "eu-west-1_sddb_SwapUsage": 128614.4, 
    "eu-west-1_sddb_TotalDiskUsage": 5368709120.0, 
    "eu-west-1_sddb_TotalMemory": 660351221.76, 
    "eu-west-1_sddb_UsedDiskUsage": 5368709101.69, 
    "eu-west-1_sddb_UsedMemory": 660348572.86, 
    "eu-west-1_sddb_WriteIOPS": 0.26, 
    "eu-west-1_sddb_WriteLatency": 1.05, 
    "eu-west-1_sddb_WriteThroughput": 2648.9
}
```

Additional Notes
----------------

This plugin requires at least python-boto 2.35.2, Ubuntu 14.04 can use [Chris Lea's PPA](https://launchpad.net/~chris-lea/+archive/ubuntu/python-boto).
