*APT Updates availble*
===
This plugin will report the number of APT updates and security updates available to the system.

Setup
---
Download AptUpdates.py into your plugin directory, usually found here: `/usr/local/share/sd-plugins`. If you are unsure of your plugin directory location, check your config.cfg, located at: `/etc/sd-agent/config.cfg`.

Metrics
---

updates - The number of APT updates available.

security - The number of APT security updates available.

Recommended alerts
---

* `updates` - Greater than X (what you deem is high enough to warrant an alert).

* `security` - Greater than X (what you deem is high enough to warrant an alert).


