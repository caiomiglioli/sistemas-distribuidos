#!/bin/sh
sudo apt update
sudo apt install docker docker-compose
docker run --name rabbitmq_sd -p 5672:5672 rabbitmq