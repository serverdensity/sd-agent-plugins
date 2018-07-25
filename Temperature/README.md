Temperature Monitor
===

This plugin is for [lm-sensors](http://www.lm-sensors.org/) and Raspberry Pi.

For hard disk temperature tests [smartctl](http://www.smartmontools.org/) is required.

Setup
---

To to check hard disk temperatures using smartctl the plugin needs to execute the following
using sudo:

`sudo smartctl --all /dev/DEVICE -s on`

Depending on how you are running the agent you maybe need to give the sd-agent more permissions.
[plugins requiring sudo](https://support.serverdensity.com/hc/en-us/articles/360001066843)
has more information.

Linux
---
1. You must have installed [lm-sensors](http://www.lm-sensors.org/).
2. Ensure the command `sensors` outputs the correct data.
3. You must have smartmontools installed [smartctl](http://www.smartmontools.org/)
4. `smartctl` outputs correct data

Raspberry Pi
---
Have the file ```/sys/class/thermal/thermal_zone0/temp``` available to read.

Metrics
---
CPU hard drive and motherboard temperatures.

Recommended alerts
---
* `Core *` - CPU temperatues, if this suddenly spikes or increases a fan might be broken.
* `temp*` - Sensors on the mainboard, raised values might indicate air intake into the case is broken.
* `/dev/*d*` - Disk temperatures, raised value means disk needs more airflow or less utilisation

Configuration
---
```
[Temperature]
# c(elsius) f(ahrenheit) k(elvin)
scale: c
# report CPU temperature values
cpus: yes
# report other temperature stats from the command "sensors"
other: no
# specify adapters to report on, you will need to change these
adapters: f75375-i2c-0-2d
# the following requires sudo access - https://support.serverdensity.com/hc/en-us/articles/360001066843
# set the disks, leave blank to test all disks, 'no' disable disk checks
disks: '/dev/sda,/dev/hda'
```
