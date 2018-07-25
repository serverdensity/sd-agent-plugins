# Network Interface Plugin

This plugin attempts to determine the status of all network interfaces on the server via `ip link`, except for the loopback device. The status is then returned as an integer so that this can be graphed. The device name is used as the metric name.

## Setup
1. Download [NetworkInterface.py](NetworkInterface.py) into your plugin directory. If you are unsure of your plugin directory location, check your config.cfg, located at: /etc/sd-agent/config.cfg
1. Restart sd-agent

More information regarding custom plugins can be found [here](https://support.serverdensity.com/hc/en-us/articles/360001083186)

## Status Mapping
 | State | Integer |
 |----|----|
 | `UP` | 0 |
 | `DOWN` | 1 |
 | `UNKNOWN` | 2 |

## Check Status
A `check_status` metric is also returned. If there was an error with the check, `check_status` will be returned as `1`. Else, if there were no errors and the check completes successfully `check_status` will be returned as `0`.

## Recommended Alerts
`NetworkInterface > eth0` `!=` `0`

## Example Output
Example output indicating all network adaptors are UP and the check completed successfully.
```python
{
    "check_status": 0,
    "docker0": 0,
    "eth0": 0,
    "vethab932d5@if4": 0
}
```
