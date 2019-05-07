#!/bin/bash

# create webserver instance
. ./openrc.sh; ansible-playbook --ask-become-pass web_server.yaml

echo "The webserver instance is created"

# create dbserver instance
. ./openrc.sh; ansible-playbook --ask-become-pass db_server.yaml

echo "The dbserver instance is created"

# create harvester1 instance
. ./openrc.sh; ansible-playbook --ask-become-pass harvester1.yaml

echo "The harvester1 instance is created"

# create harvester2 instance
. ./openrc.sh; ansible-playbook --ask-become-pass harvester2.yaml

echo "The harvester2 instance is created"