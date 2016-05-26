mdadm Basic Monitor
===

This plugin gets stats from /proc/mdstat and for each md* device returns a 1 if the amount of raid disks does not equal the amount of non degraded disks. If the amount of raid disks equals the amount of non degraded disks a 0 is returned 

Requirements 
---
* Python 2.6+ 
* mdstat - https://pypi.python.org/pypi/mdstat/

Installation - v1 Agent
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

Installation - v2 Agent
---
1. Check if you have mdstat installed in the agent venv. Run:
  ```
source /usr/share/python/sd-agent/bin/activate 
python -mdstat
deactivate
```
  When you hit return, if the command completes and you get no errors then you have the module already installed and can skip to step 3 below.
Otherwise you'll get the following error:
  ```
/usr/bin/python: No module named mdstat
```

2. Install mdstat:
  ```
source /usr/share/python/sd-agent/bin/activate 
pip install mdstat
deactivate
```

3. Download the [Mdadm.py](Mdadm.py) plugin file into your [Server Density agent plugin directory](/README.md).

4. Restart the agent

Recommended alerts
---
* `md*_degraded` - Not equal to 0 where * is equal to your md device number. 

Configuration
---
None