OpenManage RAID
===

This plugin is for OpenManage RAID. 

Setup
---
Depending on how you are running the agent you maybe need to give the sd-agent more permissions. [Plugins requiring sudo](https://support.serverdensity.com/hc/en-us/articles/201253683-Plugins-requiring-sudo) has more information.

Configuration (Optional) v2 Agent
---
Configuration is optional. If no config options are found then the defaults are used which are shown below
* If you want to override the defaults add the following config value to `/etc/sd-agent/plugins.cfg` at the end of the file.  
```
[OpenManage]
disk_count: 2
om_report: /opt/dell/srvadmin/bin/omreport
```
You can read more about setting config values in our [help docs](https://support.serverdensity.com/hc/en-us/articles/201003178-Agent-config-variables)
* Download the [OpenManage.py](OpenManage.py) plugin file into your [Server Density agent plugin directory](/README.md).
* Restart the agent.

Metrics
---
`stateX` where `X` is the pdisk number, typically `0:1` or similar - Returns the state of the pdisk
`check` - Returns `OK` or `FAIL`. `FAIL` is returned if the amount of disks seen in the response is less than the configured `disk_count` (default 2) or if an error is seen when executing the plugin.

Recommended alerts
---
* `check` != `OK`
* `stateX` != `Online`
