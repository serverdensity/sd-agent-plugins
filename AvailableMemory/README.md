#Available memory Plugin

**_This plugin has been deprecated as this metric is now available by default with the v2 agent_**

This is a very simple plugin that provides an accurate available memory metric based on the `free` command. It solves the problem of the default memory metrics not accounting for buffers/cached memory, which can cause low memory alerts on servers that are holding a large cache.

Any version of free older than 3.3.10 will use buffers/cache to calculate the available memory. From version 3.3.10 it will instead use available memory that is now readily available and is more reliable. 

Please read a more [in-depth discussion here](http://unix.stackexchange.com/a/180501)
