FROM osgeo/gdal

ENV DEBIAN_FRONTEND noninteractive

USER root

EXPOSE 5050/udp
EXPOSE 5050/tcp