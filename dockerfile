FROM geopython/pygeoapi

ENV DEBIAN_FRONTEND noninteractive

USER root

RUN mkdir -p /usr/src/backend

#copy requirements
COPY requirements.txt /usr/src/requirements.txt 

#copy process
COPY era_critical_infrastructure_analysis.py pygeoapi/process/era_critical_infrastructure_analysis.py 

#copy plugin script
RUN rm -rf pygeoapi/plugin.py
COPY plugin.py pygeoapi/plugin.py

#copy config file
#RUN rm -rf pygeoapi-config.yml
#COPY pyGeoAPICFGDOCKER.yml pyGeoAPICFGDOCKER.yml
COPY pyGeoAPICFGDOCKER.yml local.config.yml

#copy api description
#COPY pyGeoAPIOpenAPIDESC.yml pyGeoAPIOpenAPIDESC.yml
COPY pyGeoAPICFGDOCKER.yml local.openapi.yml

#copy data
COPY portolan.geojson portolan.geojson 

#install python packages
RUN pip3 install --no-cache-dir -r /usr/src/requirements.txt

#job manager folder
RUN mkdir /pygeoapi/pygeoapi/temp/

#configure environment
ENV PYGEOAPI_CONFIG=pyGeoAPICFGDOCKER.yml

#expose ports
EXPOSE 5000/udp
EXPOSE 5000/tcp