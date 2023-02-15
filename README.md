# A pygeoapi backend for RIESGOS processes

## Overview
The repository offers a process for the [pygeoapi](https://pygeoapi.io/) which can execute processes of the [RIESGOS](https://www.riesgos.de/de/) project which are contained in a docker image. Directories for inputs and ouputs get mounted into the docker container started by the process. The process itself and its results can be controlled and accessed via the pygeoapi interface which implements concepts of the [OGC API Processes](https://ogcapi.ogc.org/processes/) standard. 

## Setup
The [tum-era-critical-infrastructure-analysis](https://github.com/52North/tum-era-critical-infrastructure-analysis) docker image provided by 
52°North Spatial Information Research GmbH and the image provided in this repository must be present.

