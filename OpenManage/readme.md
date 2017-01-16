OpenManage RAID
===

This plugin is for OpenManage RAID.

Setup
---
Depending on how you are running the agent you may need to give the sd-agent more permissions. [Plugins requiring sudo](https://support.serverdensity.com/hc/en-us/articles/201253683-Plugins-requiring-sudo) has more information.

Installation - v2 Agent
---
* Download the [OpenManage.py](OpenManage.py) plugin file into your [Server Density agent plugin directory](/README.md).
* (Optional) Configure the plugin - see below.
* Restart the agent.


Configuration (Optional) v2 Agent
---
Configuration is optional. If no config options are found then the defaults are used which are the values shown below
If you want to override the defaults add the following config options with your required values to `/etc/sd-agent/plugins.cfg` at the end of the file.
`disk_count` - the amount of disks to be expected by the plugin.
`om_report` - the location of omreport, if it does not match the default.
```
[OpenManage]
disk_count: 2
om_report: /opt/dell/srvadmin/bin/omreport
```
You can read more about setting config values for custom plugins in our [help docs](https://support.serverdensity.com/hc/en-us/articles/213074438-Information-about-Custom-Plugins)

Metrics
---
* `stateX` where `X` is the pdisk number, typically `0:1` or similar - Returns the state of the pdisk as an int. See below for more info
* `check` - Returns `0` or `1`. `1` is returned if the amount of disks seen in the response is less than the configured `disk_count` (default 2) or if an error is seen when executing the plugin else `0` is returned.

Recommended alerts
---
* `check` != `0`
* `stateX` != `0`

Disk States
---
States taken from [here](http://www.dell.com/support/manuals/uk/en/ukbsdt1/dell-openmanage-server-administrator-v8.3/OMSS_UG/Physical-Disk-Or-Physical-Device-Properties?guid=GUID-D4CFE840-7128-46D2-B21C-39741581DABB&lang=en-us)
*`0` - Online
*`1` - Degraded
*`2` - Failed
*`3` - Offline
*`4` - Rebuilding
*`5` - Incompatible
*`6` - Removed
*`7` - Clear
*`8` - SMART Alert Detected
*`9` - Foreign
*`10` - Unsupported
*`11` - Replacing
*`12` - Non-RAID
*`13` - Unknown
*`14` - Ready
*`15` - Disk state could not be determined - The disk state could not be determined by the plugin as it does not match one of the above states.
