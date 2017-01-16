Mount Point Basic Monitor
===

This plugin gets stats from df and returns all mount points in a string. Use 'does not contain' alerts to notify you when your mount point is no longer available. You cannot graph this data as Server Density cannot graph string data.
 
Requirements 
---
* Python 2.6+ 

Installation - v1 Agent
---
1. Configure your agent for plugin use

2. Download the [MountPoints.py](MountPoints.py) plugin file into your [Server Density agent plugin directory](https://support.serverdensity.com/hc/en-us/articles/213074438).

3. Restart the agent

Installation - v2 Agent
---
1. Configure your agent for plugin use. Instructions can be found [here](https://support.serverdensity.com/hc/en-us/articles/213074438)

2. Download the [MountPoints.py](MountPoints.py) plugin file into your [Server Density agent plugin directory](https://support.serverdensity.com/hc/en-us/articles/213074438).

3. Restart the agent using the following command: `service sd-agent restart`

Recommended alerts
---
* `mounted` - Does not contain `*` where * is the mount point you wish to monitor. 

Configuration
---
None