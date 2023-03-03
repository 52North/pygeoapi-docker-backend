FROM geopython/pygeoapi

ENV DEBIAN_FRONTEND noninteractive

USER root

RUN mkdir -p /usr/src/backend

#copy requirements
COPY requirements.txt /usr/src/requirements.txt 

#copy process
COPY era_critical_infrastructure_analysis.py pygeoapi/process/era_critical_infrastructure_analysis.py 
COPY echo.py pygeoapi/process/echo.py 

#copy plugin script
RUN rm -rf pygeoapi/plugin.py
COPY plugin.py pygeoapi/plugin.py

#copy config file
COPY pyGeoAPICFGDOCKER.yml local.config.yml

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