# MySQL monitoring  - Linux, Mac and FreeBSD

**_This plugin has been deprecated in favour of the [official MySQL plugin](https://support.serverdensity.com/hc/en-us/articles/211821268)_**

## 1. Dependencies

Our MySQL plugin uses MySQLdb module to interact with MySQL. You must have this installed to use the MySQL monitoring functionality.

a) Installation - package managed (try this first)

CentOS, Fedora, RHEL:

    yum install python-devel
    yum install MySQL-python

Debian, Ubuntu:

    apt-get install python-dev
    apt-get install python-mysqldb

b) Installation - manual (try this if option a) above does not work)

Download MySQLdb and install it: This will require the Python build tools and MySQL development headers.

    python setup.py build
    python setup.py install

You will also need to set the permissions if you installed the agent using our OS packages: 

    chmod -R 777 /usr/bin/sd-agent/

c) Installation - manual (dependancies)

If you get errors in step b) above, you may need to install some extra packages. Install the Python build tools and MySQL headers using your OS package management:

CentOS, Fedora, RHEL:

    yum install python-devel
    yum install mysql-devel

Debian, Ubuntu:

    apt-get install python-dev
    apt-get install mysql-devel
Then install the Python setuptools by following the instructions on the website. You will then be able to go back to step b).


## 2. Agent configuration

The agent /etc/sd-agent/config.cfg file requires 3 additional config lines to be completed to allow the agent to connect to your MySQL server. In other words, the mysql config section under `[Main]` should be empty and the section below should be added to config.cfg

    [MySQLServer]
    mysql_server:
    mysql_user:
    mysql_pass:

Fill out the details for each line for a MySQL user. Your `mysql_server` will generally be `localhost` unless you want the agent to connect to a remote server.

    [MySQLServer]
    mysql_server: localhost
    mysql_user: my_username
    mysql_pass: my_password

### Connecting through SSL
If you want to connect to the server via SSL you have to set the following to parameters. There are instructions on how to create SSL certificates in [MySQL manual](http://dev.mysql.com/doc/refman/5.5/en/creating-ssl-certs.html)
    
    mysql_ssl_cert: /path/to/cert.pem
    mysql_ssl_key: /path/to/key.pem

You'll also have to add the following lines to your `my.cnf` file.
    
    ssl-ca=/etc/mysql-ssl/ca-cert.pem
    ssl-cert=/etc/mysql-ssl/server-cert.pem
    ssl-key=/etc/mysql-ssl/server-key.pem

### Custom ports and sockets
You can specify a custom port and/or socket if you are not running the default. You do this by adding 2 new config options to the config file underneath the existing options e.g, the default port is `3306`: 

    mysql_port: 3307
    mysql_socket: /tmp/mysql.sock

### Monitoring extra metrics
You can add further parameters to monitor if you would like by including the following two parameters. The metrics need to be comma-separated as below. `mysql_include_per_s` gives you the metric per second whereas `mysql_include` just gives you the counter. You can find the entire list of metrics here in the [MySQL manual](http://dev.mysql.com/doc/refman/5.1/en/server-status-variables.html#statvar_Slow_queries).

    mysql_include_per_s: Com_commit, Bytes_sent, Com_analyze
    mysql_include: Com_commit, Com_truncate

### Users

You can use any user to connect to the database that has the process privilege. The user will need process privilege to be able to gather `Checkpoint age` from the command `'SHOW ENGINE INNODB STATUS'`. We recommend that you create a specific user with this privilege. See the [MySQL documentation for user management instructions](http://dev.mysql.com/doc/refman/5.1/en/user-account-management.html). In short the command that needs to be run in the database is the following `GRANT PROCESS ON * . * TO ‘[username]’@'[server]’;`


## 3. Restart agent

[Restart the agent](https://serverdensity.zendesk.com/hc/en-us/articles/201008977-Restarting-the-agent) to start the monitoring. Using replication? [Make sure you set up the right alerts](http://support.serverdensity.com/hc/en-us/articles/201179067-MySQL-replication-monitoring).

## 4. Add graphs

Click the name of your server from the Devices list in your Server Density account then go to the Metrics tab. Click the + Graph button on the right then choose the MySQL metrics to display the graphs. The metrics will also be available to select when [building dashboard graphs](https://support.serverdensity.com/hc/en-us/articles/201895006-Dashboard-graphs).

## 5. Available Metrics from the start

    {
        "Checkpoint age": 0,
        "Com commit/s": 0,
        "Com delete/s": 0,
        "Com rollback/s": 0,
        "Com select/s": 0,
        "Com update/s": 0,
        "Connection usage %": 0.6622516556291391,
        "Key cache hit ratio": 66.66666666666667,
        "Key reads/s": 0,
        "Queries per second": 0,
        "Questions/s": 0,
        "RW ratio": 0,
        "Reads/s": 0,
        "Slow queries": 0.0,
        "Tmp Cache Hit Ratio": 100.0,
        "Transactions/s": 0,
        "Uptime": 182811.0,
        "Writes/s": 0,
        "aborted clients": 6.0,
        "aborted connects": 0.0,
        "buffer pool pages data": 148.0,
        "buffer pool pages dirty": 0.0,
        "buffer pool pages free": 8043.0,
        "buffer pool pages total": 8191.0,
        "created tmp tables": 36406.0,
        "created tmp tables on disk": 0.0,
        "max connections": 151.0,
        "max used connections": 6.0,
        "open files": 16.0,
        "qcache free memory": 1031336.0,
        "qcache hits": 0.0,
        "qcache hits/s": 0,
        "qcache in cache": 0.0,
        "qcache not cached": 1357.0,
        "select full join": 0.0,
        "slave running": 0,
        "table locks waited": 0.0,
        "threads connected": 2.0,
        "threads running": 1.0,
        "version": [
            "5",
            "6",
            "21"
        ]
    }

Some of these metrics have been calculated and will thus be described below. 

* All metrics that are listed as per second uses a counter that was executed since last check and the elapsed time since last check. 
*  **Connection Usage** - This is the current connection count (`threads running`) as a percentage of `max connections`. If you are close to 100% you have an immense load or you might consider to increase the `max connections`.
*  **Key cache hit ratio** - This is the proportion of index values that are read from cache instead of from disk. 
*  **Reads/s** - This is a calculation of the number of reads that's done on the MySQL server. It's a combination of `Com_select`, `Qcache_hits`.
*  **Writes/s** - This is a calculation of the number of writes that's done on the MySQL server. It's a combination of `Com_insert`, `Com_replace`, `Com_update`, `Com_delete`.
*  **RW ratio** - This is the Read and Write ratio. This is simply the ratio of reads and writes as how reads and writes are defined above.
*  **Tmp Cache Hit Ratio** - This is the proportion of temp tables that were created in cache or on disk. If the value is 100% it means that all tables were created in cache.

For a more in-depth guide of understanding what these metrics mean please check out the blog post on [How to monitor MySQL](#)
