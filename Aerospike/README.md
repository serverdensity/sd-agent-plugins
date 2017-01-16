Aerospike Monitor
===

This plugin is for [Aerospike](http://www.aerospike.com/). It is based on the
detailed list of metrics available for namespace and overall health&service [Aerospike Metrics](http://www.aerospike.com/docs/reference/metrics).

Setup
---
You will need to install the Aerospike python module in your sd-agent virtual environment to start gathering Aerospike metrics.  
1. Ensure that you have properly configured custom plugins. If you are unsure, follow this [guide](https://support.serverdensity.com/hc/en-us/articles/213074438) 
1. Activate the vitual environment using the following command: `. /usr/share/python/sd-agent/bin/activate` 
2. Once you have activated the virtual environment install the Aerospike module using the folowing command: `pip install aerospike`
3. Use the `deactivate` command to close the virtual environment

Ensure you have the correct permissions to before attempting to install the Aerospike module.

Metrics
---
- Overall database health and service metrics
- Health metrics for a particular namespace

Recommended alerts
---
http://www.aerospike.com/docs/operations/monitor/key_metrics

Configuration file : /etc/sd-agent/plugins.cfg
---
[Aerospike]  
host: localhost  
port: 3000  
namespaces: test1,test2
