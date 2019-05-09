#!/bin/bash
curl -X POST -H "Content-Type: application/json" http://admin:admin@127.0.0.1:5984/_cluster_setup -d '{"action": "enable_cluster", "bind_address":"0.0.0.0", "username": "admin", "password":"admin"}'

curl -X POST -H "Content-Type: application/json" http://admin:admin@127.0.0.1:5984/_cluster_setup -d '{"action": "add_node", "host":"$1", "port": "5984", "username": "admin", "password":"admin"}'
curl -X POST -H "Content-Type: application/json" http://admin:admin@127.0.0.1:5984/_cluster_setup -d '{"action": "add_node", "host":"$2", "port": "5984", "username": "admin", "password":"admin"}'

curl -X POST -H "Content-Type: application/json" http://admin:admin@127.0.0.1:5984/_cluster_setup -d '{"action": "finish_cluster"}'
