#!/bin/bash

# remove the exited hosts.ini 
touch Config/inventory/hosts.ini
rm Config/inventory/hosts.ini

# create webserver instance
. ./openrc.sh; ansible-playbook --ask-become-pass NeCTAR/webServer.yaml

echo "The webserver instance is created"

# create dbserver instance
. ./openrc.sh; ansible-playbook --ask-become-pass NeCTAR/dbServer.yaml

echo "The dbserver instance is created"

# create harvester1 instance
. ./openrc.sh; ansible-playbook --ask-become-pass NeCTAR/harvester1.yaml

echo "The harvester1 instance is created"

# create harvester2 instance
. ./openrc.sh; ansible-playbook --ask-become-pass NeCTAR/harvester2.yaml

echo "The harvester2 instance is created"

ansible-playbook -i Config/inventory/hosts.ini -u ubuntu Config/config_harvester.yml