Foocast Server Density plugin
=============================

This plugin allows to monitor wind and precipitation intensity on different locations. It was built with datacenters in mind but can monitor any other location. The metrics returned are the maximum values expected on the next 7 days. To retrieve weather forecast data uses [Forecast.IO](https://forecast.io/) and uses [ForecastIO Python](https://github.com/dvdme/forecastiopy) to query their API.

Setup
-----

1. Install python-geopy `sudo apt-get install python-geopy`
2. Install python-pip `sudo apt-get install python-pip` and then forecastiopy `pip install forecastiopy`
3. Drop the Foocast.py script in your plugin directory, most likely `/usr/local/share/sd-plugins/`
4. Configure the plugin YAML file, for example in `/etc/sd-agent/conf.d/datacenters.yaml`:

    ```
    ---
    google:
      ie:
        - location: Dublin, Ireland
      nl:
        - location: Eemshaven, Netherlands
      fi:
        - location: Hamina, Finland
    ```
5. Configure the plugin, in `/etc/sd-agent/plugins.cfg`:

    ```
    [Foocast]
    cfg_file = /etc/sd-agent/conf.d/datacenters.yaml
    forecastio_key = XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
    run_interval = 3600
    ```
6. Restart the agent to apply changes `sudo service sd-agent restart`

Troubleshooting
---------------

You can run the script directly from the command line to collect the metrics:

```
$ python Foocast.py {
    "google_fi_precipIntensity": "0.3785", 
    "google_fi_windSpeed": "6666666.79", 
    "google_ie_precipIntensity": "0.4039", 
    "google_ie_windSpeed": "7.63", 
    "google_nl_precipIntensity": "0.3658", 
    "google_nl_windSpeed": "7.83"
} 
```

Additional Notes
----------------
Foocast.IO limits API requests per day on free accounts. Adjust `run_interval`
depending on the number of locations you need to monitor.

