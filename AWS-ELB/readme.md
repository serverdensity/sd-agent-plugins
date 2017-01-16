## AWS ELB Server Density Plugin



This plugin allows you to monitor AWS ELBv1 (Classic load balancers) instances. The plugin does not currently support ELBv2 (Application load balancers). It uses [Python Boto](http://boto.cloudhackers.com/en/latest/) to query AWS CloudWatch.

Every minute it pulls the sum of the different metrics CloudWatch provides for ELB. 

You can't install any agent on a ELB loadbalancer so therefore you will have to install this plugin on another server that has an agent. 

In the configuration you can get data from multiple ELB instances by separating them with a a comma. Due to the nature of Boto making a request for each metric it's advisable to not monitor too many ELB instances to allow the agent to make postbacks every minute. 

You can also find more information about the metrics that [ELB provides](http://docs.aws.amazon.com/ElasticLoadBalancing/latest/DeveloperGuide/elb-cloudwatch-metrics.html)

### Setup
1. Install python-boto `sudo apt-get / yum install python-boto`
2. Configure the plugin in `/etc/sd-agent/plugins.cfg` 
    ```
    [ELB]
    aws_access_key_id: ACCESS_TOKEN
    aws_secret_access_key: SECRET
    elb_identifier_region: ELB_INSTANCE:REGION,ELB_INSTANCE:REGION
    ```
3. Download the ELB.py script to your plugin directory using this command `https://raw.githubusercontent.com/serverdensity/sd-agent-plugins/master/AWS-ELB/ELB.py`. Your plugin directory will most likely be located at `/usr/local/share/sd-plugins/`. Check your `config.cfg` if you're unsure. If the plugin destination is empty, create a directory in your desired location and put that path in `config.cfg`
4. Restart the agent to apply changes `sudo service sd-agent restart`.

You can find out how to get access and secret access keys [here](http://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSGettingStartedGuide/AWSCredentials.html)

ELB_INSTANCE is the name of the ELB instance, REGION is the where the ELB is based. You can find both of these in the AWS UI or with the following command using the AWS api: `aws elb describe-load-balancers`

### Troubleshooting

You can run the script directly from the command line to see what metrics are being sent. 

```
python ELB.py -k ACCESS_KEY -p SECRET -e ELB_INSTANCE:REGION
{
    "ELB-test_backend_connection_errors": 0.0,
    "ELB-test_healthy_host_count": 2.0,
    "ELB-test_http_code_backend_2xx": 157.0,
    "ELB-test_http_code_backend_3xx": 79.0,
    "ELB-test_http_code_backend_4xx": 0.0,
    "ELB-test_http_code_backend_5xx": 0.0,
    "ELB-test_http_code_elb_4xx": 0.0,
    "ELB-test_http_code_elb_5xx": 0.0,
    "ELB-test_latency": 2.24,
    "ELB-test_request_count": 236.0,
    "ELB-test_spillover_count": 0.0,
    "ELB-test_surge_queue_length": 0.0,
    "ELB-test_unhealthy_host_count": 0.0
}
```
