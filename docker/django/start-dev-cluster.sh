#!/bin/bash

# ludensprod.com fix
bash docker/django/ludensprod-fix.sh

# run cluster
python manage.py qcluster