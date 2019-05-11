#!/bin/bash

# remove the existed hosts.ini 
touch Config/inventory/hosts.ini
rm Config/inventory/hosts.ini

# remove the existed var.yml
touch Config/var/var.yml
rm Config/var/var.yml

# create 4 instance
. ./openrc.sh; ansible-playbook --ask-become-pass NewNeCTAR/createInstances.yaml

echo "COUNT_NODES: 3" >> Config/var/var.yml

sleep 180

cd Config

ansible-playbook -i ./inventory/hosts.ini -u ubuntu ./config.yml