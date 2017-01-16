Available Entropy
===
This plugin is for reporting status of "Available Entropy" on system.
Entropy is the measure of the random numbers available from /dev/urandom.

Used by: SSL connections, cryptographic services, etc.

**ONLY WORKS ON LINUX**

Setup
---
Download Entropy.py into your plugin directory, usually found here: `/usr/local/share/sd-plugins`. If you are unsure of your plugin directory location, check your config.cfg, located at: `/etc/sd-agent/config.cfg`

Metrics
---

Available

Recommended alerts
---

* `available` - Greater than 1000 (depends on your needs).

Random number generators (software)
---
[haveged](http://www.issihosts.com/haveged/)
[rng-tools](https://www.gnu.org/software/hurd/user/tlecarrour/rng-tools.html)

There are also packages for **yum** and **apt** available!
