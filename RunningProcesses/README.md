# Running Processes

This plugin monitors the existence of running processes using `pgrep`. It does not care about the number of child processes, just returns a 1 if `pgrep process_name` has results, and a 0 if not.

## Usage

To install this plugin, add a config section to your `/etc/sd-agent/config.cfg` file. The plugin requires only one config value, which is a comma separated list of process names to pass to pgrep.

```
[Running Processes]
process_list: foo,bar,baz
```

Then place the plugin file into your plugin directory and restart the agent.

If this is your first plugin installation, read the general plug instructions: https://github.com/serverdensity/sd-agent-plugins
