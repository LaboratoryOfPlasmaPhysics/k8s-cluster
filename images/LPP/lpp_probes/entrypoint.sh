#!/bin/bash
/usr/bin/lpp-services-status.py &
while true
do
   /usr/bin/redmine-stats.py
   sleep 60
done
