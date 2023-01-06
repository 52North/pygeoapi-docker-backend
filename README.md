# A pygeoapi Backend for RIESGOS Processes

## Overview
tbd. 

## Setup
The [tum-era-critical-infrastructure-analysis](https://github.com/52North/tum-era-critical-infrastructure-analysis) docker image provided by 
52°North Spatial Information Research GmbH must be present.

To be able to start the processes with the pygeoapi a version of the pygeoapi along with its requirements must be installed:
```
pip install pygeoapi
```
Details about the configuration of the pygeoapi can be found in the [documentation](https://docs.pygeoapi.io/en/stable/index.html).
There are a few additional steps to perform to enbale the execution of RIESGOS-processes via the pygeoapi.

Step 1: Copy the era_critical_infrastructure_analysis.py into the processes folder of the pygeoapi.

Step 2: Add the following to resources section the .config of the pygeoapi:
```
cia: 
        type: process  
        processor:
            name: cia
```

Step 3: Add the following to the plugin.py ```PLUGINS``` section:
```
'process': { 
        'cia': 'pygeoapi.process.era_critical_infrastructure_analysis.ciaProcessor'
    }
 ```
 
 The cia process should now be pluged in correctly. I should be visible in the processes section of the pygeoapi web-interface and be executeable, for example using cURL.

## Operation
tbd. test
