#!/bin/bash

cp -r ./src/* /opt/gpkg
touch /usr/bin/gpkg

cp ./gpkg /usr/bin
chmod +x /usr/bin/gpkg
