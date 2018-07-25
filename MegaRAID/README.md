MegaRAID Basic Monitor
===

This plugin is for MegaRAID

Setup
---
Depending on how you are running the agent you maybe need to give the sd-agent more permissions.
[plugins requiring sudo](https://support.serverdensity.com/hc/en-us/articles/360001066843)
has more information.

Linux
---
Ensure the following command is installed and outputs correctly:

```/opt/MegaRAID/MegaCli/MegaCli64 -LDInfo -Lall -aALL ```

Recommended alerts
---
* `state` - Not equal to "Optimal"

Configuration
---
None
