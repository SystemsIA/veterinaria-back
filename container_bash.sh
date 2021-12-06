#!/usr/bin/sh
docker-compose -f local.yml run  -u "$(id -u):$(id -g)" django bash
