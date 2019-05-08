#!/bin/bash

# remove the existed hosts.ini 
touch Config/inventory/hosts.ini
rm Config/inventory/hosts.ini

# remove the existed var.yml
touch Config/var/var.yml
rm Config/var/var.yml

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

echo "COUNT_NODES: 3" >> Config/var/var.yml

sleep 60

cd Config

ansible-playbook -i ./inventory/hosts.ini -u ubuntu ./config_harvester.yml