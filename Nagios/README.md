Nagios Server Density plugin
=============================

This plugin allows to monitor your Nagios server availability and performance.

Setup
-----

1. Install the Server Density agent.
2. Drop the Nagios.py script in your plugin directory, most likely `/usr/local/share/sd-plugins/`. This path is configure in `/etc/sd-agent/config.cfg`.
2. Configure the plugin, in `/etc/sd-agent/plugins.cfg`:

    ```
    [Nagios]
    cmd_path = /usr/local/nagios/bin/nagiostats
    ```
6. Restart the agent to apply changes `sudo service sd-agent restart`.
7. Configure your alerts and graphs in Server Density app.

Troubleshooting
---------------

You can run the script directly from the command line to collect the metrics:

```
$ python /usr/local/share/sd-plugins/Nagios.py 
{
    "Active Host Checks Cached": 0, 
    "Active Host Checks On-demand": 0, 
    "Active Host Checks Parallel": 0, 
    "Active Host Checks Scheduled": 0, 
    "Active Host Checks Serial": 0, 
    "Active Host Checks Total": 0, 
    "Active Host Execution Time": 4.001, 
    "Active Host Latency": 0.002, 
    "Active Host State Change": 0.0, 
    "Active Hosts": 0, 
    "Active Service Checks Cached": 0, 
    "Active Service Checks On-demand": 0, 
    "Active Service Checks Scheduled": 2, 
    "Active Service Checks Total": 2, 
    "Active Service Execution Time": 0.001, 
    "Active Service Latency": 0.0, 
    "Active Service State Change": 0.0, 
    "Active Services": 2, 
    "External Commands": 0, 
    "Host Passively Checked": 0, 
    "Hosts Actively Checked": 1, 
    "Hosts Checked": 1, 
    "Hosts Flapping": 0, 
    "Hosts In Downtime": 0, 
    "Hosts Scheduled": 1, 
    "Hosts Status Down": 0, 
    "Hosts Status Unreachable": 0, 
    "Hosts Status Up": 1, 
    "Passive Host Checks": 0, 
    "Passive Host Latency": 0.0, 
    "Passive Host State Change": 0.0, 
    "Passive Hosts": 0, 
    "Passive Service Checks": 0, 
    "Passive Service Latency": 0.0, 
    "Passive Service State Change": 0.0, 
    "Passive Services": 0, 
    "Services Actively Checked": 8, 
    "Services Checked": 8, 
    "Services Flapping": 0, 
    "Services In Downtime": 0, 
    "Services Passively Checked": 0, 
    "Services Scheduled": 8, 
    "Services Status Critical": 1, 
    "Services Status Ok": 7, 
    "Services Status Unknown": 0, 
    "Services Status Warn": 0, 
    "Total Host State Change": 0.0, 
    "Total Hosts": 1, 
    "Total Service State Change": 0.0, 
    "Total Services": 8, 
    "Uptime": 578405
}
```
