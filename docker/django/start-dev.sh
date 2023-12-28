#!/bin/bash

# ludensprod.com fix
bash docker/django/ludensprod-fix.sh

# run django server on ssl
python manage.py runsslserver 0.0.0.0:8000 --certificate /ssl/$SSL_CERTIFICATE_FILE --key /ssl/$SSL_CERTIFICATE_KEY