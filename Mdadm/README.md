mdadm Basic Monitor
===

This plugin gets stats from /proc/mdstat

Requirements 
---
* mdstat - https://pypi.python.org/pypi/mdstat/

Installation
---
1. Check if you have mdstat installed. Run:
  ```
python -mdstat
```
  When you hit return, if the command completes and you get no errors then you have the module already installed and can skip to step 3 below.
Otherwise you'll get the following error:
  ```
/usr/bin/python: No module named mdstat
```

2. Install mdstat:
  ```
pip install mdstat
```

3. Download the [Mdadm.py](Mdadm.py) plugin file into your [Server Density agent plugin directory](/README.md).

4. Restart the agent

Recommended alerts
---
* `md*_degraded` - Not equal to "false"

Configuration
---
None