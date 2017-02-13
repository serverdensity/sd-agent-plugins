Icinga2 Server Density plugin
=============================

This plugin allows to monitor your Icinga2 server availability and performance.
See the Nagios plugin for Icinga1 monitoring.

Prerequesites
-------------
Icinga2 with API module enabled and configured. See [Icinga2 API doc](http://docs.icinga.org/icinga2/snapshot/doc/module/icinga2/chapter/icinga2-api) for detailed steps.

Setup
-----

1. Install the Server Density agent.
2. Drop the Icinga.py script in your plugin directory, most likely `/usr/local/share/sd-plugins/`. This path is configure in `/etc/sd-agent/config.cfg`.
2. Configure the plugin, in `/etc/sd-agent/plugins.cfg`:

    ```
    [Icinga]
    api_user = root
    api_passwd = your_password
    # you will need FQDN to match the cert CN 
    api_stats_url = https://your_fqdn:5665/v1/status
    # Icinga PKI CA cert
    icinga_ca_crt = /etc/icinga2/pki/ca.crt
    ```
6. Restart the agent to apply changes `sudo service sd-agent restart`.
7. Configure your alerts and graphs in Server Density app.

Troubleshooting
---------------

You can run the script directly from the command line to collect the metrics:

```
$ python /usr/local/share/sd-plugins/Icinga.py
{
    "active_host_checks": 0.016666666666666666, 
    "active_host_checks_15min": 15.0, 
    "active_host_checks_1min": 1.0, 
    "active_host_checks_5min": 5.0, 
    "active_service_checks": 0.2, 
    "active_service_checks_15min": 180.0, 
    "active_service_checks_1min": 12.0, 
    "active_service_checks_5min": 60.0, 
    "avg_execution_time": 0.3865975538889567, 
    "avg_latency": 0.0, 
    "max_execution_time": 0.0, 
    "max_latency": 0.0, 
    "min_execution_time": 0.0, 
    "min_latency": 0.0, 
    "num_hosts_acknowledged": 0.0, 
    "num_hosts_down": 0.0, 
    "num_hosts_flapping": 0.0, 
    "num_hosts_in_downtime": 0.0, 
    "num_hosts_pending": 0.0, 
    "num_hosts_unreachable": 0.0, 
    "num_hosts_up": 1.0, 
    "num_services_acknowledged": 0.0, 
    "num_services_critical": 0.0, 
    "num_services_flapping": 0.0, 
    "num_services_in_downtime": 0.0, 
    "num_services_ok": 11.0, 
    "num_services_pending": 0.0, 
    "num_services_unknown": 0.0, 
    "num_services_unreachable": 0.0, 
    "num_services_warning": 1.0, 
    "passive_host_checks": 0.0, 
    "passive_host_checks_15min": 0.0, 
    "passive_host_checks_1min": 0.0, 
    "passive_host_checks_5min": 0.0, 
    "passive_service_checks": 0.0, 
    "passive_service_checks_15min": 0.0, 
    "passive_service_checks_1min": 0.0, 
    "passive_service_checks_5min": 0.0, 
    "uptime": 10907.203309774399
}
```
