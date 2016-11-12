Aerospike Monitor
===

This plugin is for [Aerospike](http://www.aerospike.com/). It is based on the
detailed list of metrics available for namespace and overall health&service[Aerospike Metrics](http://www.aerospike.com/docs/reference/metrics).

Setup
---
Install aerospike module : `pip install aerospike`

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