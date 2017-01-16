BackupNinja Monitor
===

This plugin is for [backupninja](https://labs.riseup.net/code/projects/backupninja/).

Setup
---
Download BackupNinja.py into your plugin directory, usually found here: `/usr/local/share/sd-plugins`. If you are unsure of your plugin directory location, check your config.cfg, located at: `/etc/sd-agent/config.cfg`

Configuration
---
Edit Plugins.cfg, located at `/etc/sd-agent/plugins.cfg`, with the following lines of configuration. Edit to your specifications.

```
[BackupNinja]
main_log: /var/log/backupninja.log
# sequence or date
rotated_log_type: sequence
```
Recommended alerts
---
* `age` - Minutes since last backup run, -1 if unknown.
* `actions` - Number of backup actions executed.
* `error` - Number of actions that had an error.
* `fatal` - Number of actions that had a fatal error.
* `warning` - Number of actions that had a warning.