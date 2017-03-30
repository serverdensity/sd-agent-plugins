Nagios / Icinga plugin wrapper for sd-agent
==============

If you are already using Nagios and want to move to Server Density, you may not want to rewrite all your Nagios plugins. This sd-agent plugin will execute your Nagios plugins, then report the data back to Server Density.

This plugin is also compatible with Icinga plugins too.

Plugin types
------------

* **Nagios Return Value**: Where the return value is either `0` = OK, `1` = Warning, `2` = Critical or `3` = Unkown, the value will be reported back to Server Density as value of the key containing the plugin name (eg. `check_hylafax` = `2`).
* **Performance Data**: This output is in the form of `'label'=value[UOM];[warn];[crit];[min];[max]` ([see docs](http://nagiosplug.sourceforge.net/developer-guidelines.html#AEN201)). In this case, it will be returned as an additional pair. As example, the plugin `check_mailq` reports `unsent=38;10;20;0`, so an additional pair `unsent` = `38` will be reported  to Server Density. *Note*: this plugin will not support wrapping two plugins that report the performance data using the same label, the second value will overwrite the first.

Installing
----------

1. Download the `NagiosWrapper.py` plugin file and place it into your sd-agent plugin directory. If you have not installed a plugin before you need to create a directory the agent will be able to read/write to then update the `/etc/sd-agent/config.cfg` file to include the location of that directory. We recommend `/usr/local/sd-agent-plugins`.
2. Install the python module `crontab`.
3. Edit or create your `/etc/sd-agent/plugins.d/NagiosWrapper.cfg` file to include the paths to the plugins you want the agent to execute and how often they should be executed (in [crontab format](https://en.wikipedia.org/wiki/Cron#Overview)). Then restart the agent. The example below uses 2 sample plugins by default, check_sensors will be executed every 10mins and check_mailq will be executed every 2mins. This MUST be valid JSON else the plugin will fail:

```python
[NagiosWrapper]
commands: {"/usr/lib64/nagios/plugins/check_sensors": "*/10 * * * *", "/usr/bin/sd-agent/check_mailq -w 10 -c 20 -M postfix": "*/2 * * * *"}

```

The `check_mailq` plugin is installed along with Nagios. `check_sensors` is a [3rd party plugin](http://exchange.nagios.org/directory/Plugins/System-Metrics/Environmental/check_sensors/details).

Raw plugin data can be found in the Server Density UI under the Plugins tab you've installed this plugin on.

Alerts
------

**Alerting on return values**

Creating an alert when the server sensors triggers or returns a unknown state. The plugin will return 2 - CRITICAL or 3 - UNKNOWN:

1. Alerts Tab
2. Add new alert
3. Select the server reporting the data, fill in the alert form as desired
4. Select NagiosWrapper plugin from the Check pull down menu.
5. Use the Nagios plugin label for the key e.g. `check_sensors`
5. Setting the trigger to Greater than or equal to 2

**Alerting on performance values**

Creating an alert when the mail queue is not zero:

1. Alerts Tab
2. Add new alert
3. Select the server reporting the data, fill in the alert form as desired
4. Select NagiosWrapper plugin from the Check pull down menu.
5. Use the Nagios plugin label for the key, in this case `unsent`
6. Setting the trigger to Greater than 0

Troubleshooting
---------------
Two important aspects are relevant to making sure the Nagios plugins runs as expected:

1. The command line is correct. The best way to test it is to run it as `sd-agent` user:

```
$ sudo -u sd-agent /usr/lib64/nagios/plugins/check_sensors
sensor ok
```
2. Some plugins may need root permissions to run. In this case a sudo wrapper may need to be used. First add a sudoers permission, using visudo append:-
```
sd-agent ALL=NOPASSWD:/usr/lib64/nagios/plugins/check_mailq
```
then create a wrapper for the actual plugin command. The agent will execute this instead, which will "proxy" the command with the sudo prefix:

```
$ cat /usr/bin/sd-agent/check_mailq
#!/bin/bash
sudo /usr/lib64/nagios/plugins/check_mailq $@
```
