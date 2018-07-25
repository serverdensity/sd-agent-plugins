Redis Monitor
===

**_This plugin has been deprecated in favour of the [official Redis plugin](https://support.serverdensity.com/hc/en-us/articles/360001066123)_**

This plugin is for [Redis](https://www.redis.io/). It is based on the
detailed list of metrics available from the INFO command [Redis Commands](http://redis.io/commands/info).

Setup
---
This plugin uses the output from `redis-cli` using the `info` to collect data about all the available Redis databases.

Install redis module : `pip install redis`

Metrics
---
- Global informations of Redis instance  
- Queues length

Recommended alerts
---

Configuration file : /etc/sd-agent/config.cfg
---
[Redis]  
host: localhost  
port: 6379  
dbs: 0,1  
password: YourHashKey|none  
queues: key1,key2