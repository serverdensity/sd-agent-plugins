IPMI Monitor
===

This plugin is for [ipmitool](http://ipmitool.sourceforge.net/).

Setup
---

To query your local IPMI board using ipmitool the plugin needs to execute the following
using sudo:

`sudo ipmitool sensor`

Depending on how you are running the agent you maybe need to give the sd-agent more permissions.
[plugins requiring sudo](https://support.serverdensity.com/hc/en-us/articles/360001066843)
has more information.

Linux
---
1. You must have installed [ipmitool](http://ipmitool.sourceforge.net/).
2. Ensure the command `ipmitool sensor` outputs the correct data.

Metrics
---
* CPU temperature (individual)
* System temperature
* Peripheral temperature
* Fan speeds
* Powersupply status

Recommended alerts
---
* `temp-cpu-*` - CPU temperatues, if this suddenly spikes or increases a fan might be broken.
* `temp-system` - Sensors on the mainboard, raised values might indicate air intake into the case is broken.
* `temp-peripheral` - Peripheral temperatures, raised values might indicate A/C problems or a fire in your datacenter.
* `speed-fan-*` - Fan speeds (RPM), a value of 0 would indicate that your fan is broken.
* `power-supply-*` - Power supply status, a value of 0 would indicate a unplugged supply.

Configuration
---
```
[Ipmi]
# report CPU temp
cpus: yes
# report system temp
system: yes
# report peripheral temp
peripheral: yes
# report fan speeds (RPM)
fans: yes
# report power status
powersupply: yes
```
