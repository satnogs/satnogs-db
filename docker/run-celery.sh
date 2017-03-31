#!/bin/bash

celery -A db worker -B -l INFO
