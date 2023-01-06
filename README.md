# A pygeoapi backend for RIESGOS processes

## Overview
The repository offers a process for the pygeoapi which can execute processes of the [RIESGOS](https://www.riesgos.de/de/) project which are contained in a docker image. Directories for inputs and ouputs get mounted into the docker container started by the process. The process itself and its results can controlled and accessed via the pygeoapi interface which implements concepts of the [OGC API Processes](https://ogcapi.ogc.org/processes/) standard. 

## Setup
The [tum-era-critical-infrastructure-analysis](https://github.com/52North/tum-era-critical-infrastructure-analysis) docker image provided by 
52°North Spatial Information Research GmbH must be present.

To be able to start the processes with the pygeoapi a version of the pygeoapi along with its requirements must be installed:
```
pip install pygeoapi
```
Details about the configuration of the pygeoapi can be found in the [documentation](https://docs.pygeoapi.io/en/stable/index.html).
There are a few additional steps to perform to enbale the execution of RIESGOS-processes via the pygeoapi.

Step 1: Copy the ```era_critical_infrastructure_analysis.py``` into the processes directory of the pygeoapi.

Step 2: Add the following to resources section the .config of the pygeoapi:
```
cia: 
        type: process  
        processor:
            name: cia
```

Step 3: Add the following to the plugin.py ```PLUGINS``` section of the pygeoapi:
```
'process': { 
        'cia': 'pygeoapi.process.era_critical_infrastructure_analysis.ciaProcessor'
    }
 ```
 
The cia process should now be pluged in correctly. I should be visible in the processes section of the pygeoapi web-interface and be executeable, for example using cURL.
A possible request can look like this: ```curl -X POST "http://HOST:PORT/processes/cia/execution" -H "Content-Type: application/json" -d "{\"mode\": \"async\", \"inputs\":{\"hazard\": \"earthquake\", \"country\": \"ecuador\", \"intensity\": \"PATH_TO_THE_INPUTS\", \"directory\": \"PATH_TO_THE_RESULTS\"}}"```

The ```shakemap.xml``` can be used as an input for testing and should be located in the input path of the request.
