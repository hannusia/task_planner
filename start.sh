#!/bin/bash

./start_mongo.sh
./start_cassandra.sh

cd login_microservice
python authentication_service.py 

cd ../tasks
python app.py

cd ../feedback
cqlsh -f init.cql
python app.py
