#!/bin/bash

/usr/local/bin/gunicorn -w 4 app:app --bind "0.0.0.0:9999" --daemon --access-logfile /var/log/gunicorn.access.log --error-logfile /var/log/gunicorn.error.log

nginx -g 'daemon off;'