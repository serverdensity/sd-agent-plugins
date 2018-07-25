Nginx Plus
===

This plugin is for the [Nginx Plus `ngx_http_status_module` commercial status module](http://nginx.org/en/docs/http/ngx_http_status_module.html). 

Configuration
---
* You must be using [Nginx Plus](http://nginx.com/products/).
* Configure the status handler in your Nginx server configuration:
```
location = /status {
    allow 192.168.0.0/16; # permit access from local network
    deny all; # deny access from everywhere else

    status;
}
```
*  Add the following config value to `/etc/sd-agent/config.cfg` at the end of the file.  
```
[nginxplus]
nginx_status_url: http://localhost/status
```
You can read more about setting config values in our [help docs](https://support.serverdensity.com/hc/en-us/articles/360001083926)
* Download the [NginxPlus.py](NginxPlus.py) plugin file into your [Server Density agent plugin directory](/README.md).
* Restart the agent.

Metrics
---
See the the [Nginx Plus `ngx_http_status_module` commercial status module](http://nginx.org/en/docs/http/ngx_http_status_module.html) documentation for the list of metrics reported.

Recommended alerts
---
* `connections_dropped` - if this suddenly spikes or has a large value then you may be dropping a large number of connections which should be investigated.
* `connections_active` - this is the current number of connections currently active. You should benchmark your server to understand what its limits are, then set alerts appropriately.
* `requests_current` - as above, but for the number of requests being served.
* The `zone_*` metrics are reported for each of your server zones. It is useful to graph the number of requests and responses but alerts can be configured on the `zone_*_responses_5xx` metric because this gives the number of internal server errors. High numbers mean problems on the server.
* The `upstream_*` metrics are similar to the `zone_*` metrics but it is recommended to set an alert on `upstream_*_*_state` `!=` `up`. This allows you to be alerted when one of your upstream servers is down or otherwise unavailable. 
* Related to this is the `upstream_*_*_unavail` count - if this is high then many requests are failing.
