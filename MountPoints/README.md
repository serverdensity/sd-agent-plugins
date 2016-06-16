Mount Point Basic Monitor
===

This plugin gets stats from df and returns all mount points in a string. Use 'does not contain' alerts to notify you when your mount point is no longer available.
 
Requirements 
---
* Python 2.6+ 

Installation - v1 Agent
---
1. Configure your agent for plugin use

2. Download the [MountPoints.py](MountPoints.py) plugin file into your [Server Density agent plugin directory](/README.md).

3. Restart the agent

Installation - v2 Agent
---
1. Chonfigure your agent for plugin use

2. Download the [MountPoints.py](MountPoints.py) plugin file into your [Server Density agent plugin directory](/README.md).

3. Restart the agent

Recommended alerts
---
* `mounted` - Does not contain `*` where * is the mount point you wish to monitor. 

Configuration
---
None