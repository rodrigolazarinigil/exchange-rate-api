#!/bin/bash

touch /var/spool/cron/crontabs/root

echo "${CRONFREQUENCY} echo \"Hello $(date)\" >>/var/log/cron.log 2>&1" >> /var/spool/cron/crontabs/root

cp /var/spool/cron/crontabs/root /tmp/temp.txt
printenv | cat - /tmp/temp.txt | tee /var/spool/cron/crontabs/root
chmod 600 /var/spool/cron/crontabs/root

cron

export FLASK_APP=flask_app.py
flask run --host=0.0.0.0