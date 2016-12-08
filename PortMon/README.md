# ServerDensity-PortMon
Remote TCP port monitoring plugin for ServerDensity.

Tests whether a TCP port on a (potentially) remote machine can be reached from your ServerDensity-monitored host and records the time a connect() took.


## Potential Uses

ServerDensity makes it very easy to monitor the status of a given server, but it doesn't offer any tools to check connectivity to external services your application depends on.  Examples include:

*   Databases
*   SSH Tunnels
*   External APIs

This means it's possible for SD to report your hosting platform as A-OK (which technically it is) but for your website to be a smoking crater because the application can't reach some external resource.

Enter PortMon - a plugin to check your hosts can connect to TCP ports elsewhere and measure the time taken for connect() to complete.

## Configuration (v2 Agent)


Ensure that your agent is setup for custom plugins - in your config.cfg you should have something like:

```plugin_directory: /usr/local/sd-agent/plugins```

See [information about custom plugins](https://support.serverdensity.com/hc/en-us/articles/213074438-Information-about-Custom-Plugins) for more information about custom plugins and configuring the agent for use with custom plugins.

Then in `/etc/sd-agent/plugins.cfg` or `/etc/sd-agent/plugins.d/PortMon.cfg` add your config as required, an example is below:

```
[PortMon]
portmon_timeout: 5
portmon_targets: 127.0.0.1:22,my-rds-db.abcdef91p1.eu-west-1.rds.amazonaws.com:1433
```

Settings are simply:

*  `portmon_timeout` - Integer timeout for connection attempts.  If this is reached the plugin records None for that target and goes on for the next.
*  `portmon_targets` - A comma-separated list of TCP hosts/ports in the form `host:port`.

Then restart the agent.


## Configuration (Legacy v1 Agent)

Config is intentionally simple.  Create the following section in your ServerDensity agent config, usually `/etc/sd-agent/config.cfg`.

Requires plugins to be enabled - in your config.cfg have something like:

```plugin_directory: /usr/local/sd-agent/plugins```

Config looks like:

```
[PortMon]
portmon_timeout: 5
portmon_targets: 127.0.0.1:22,my-rds-db.abcdef91p1.eu-west-1.rds.amazonaws.com:1433
```

Settings are simply:

*  `portmon_timeout` - Integer timeout for connection attempts.  If this is reached the plugin records None for that target and goes on for the next.
*  `portmon_targets` - A comma-separated list of TCP hosts/ports in the form `host:port`.


## Return Values

For each target you define you'll get back a key/value pair of:

*   Key - target hostname with all periods replaced with underscores.  (Why?  Because ServerDensity doesn't support periods in the key names)
*   Value - Number of seconds it took to connect to the resource.

The values are eminently suitable for alerting and publishing on dashboard graphs, either all-in-one or separately.


## License

MIT.  See /LICENSE.


## Acknowledgements

This plugin was originally developed by [@alexmbird](https://github.com/alexmbird/) for [The Dextrous Web Ltd](https://www.dxw.com/).

