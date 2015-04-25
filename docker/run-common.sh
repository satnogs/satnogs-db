#!/bin/bash

find ./staticfiles -mindepth 1 -not -name '.gitkeep'| xargs rm -rf
./manage.py collectstatic --noinput
./manage.py migrate --noinput
