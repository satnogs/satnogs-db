#!/bin/sh

./docker/run-common.sh
gunicorn db.wsgi:application -b 0.0.0.0:80 -w 2 --log-file -
