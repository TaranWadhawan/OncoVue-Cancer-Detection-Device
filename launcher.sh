#!/bin/bash

until ping -c 1 8.8.8.8 >/dev/null 2>&1
do 
    echo "waiting for internet"
    sleep 3
done

sleep 3
exort QT_QPA_PLATFORM=xcb
cd /home/oncovue/Downloads/Final_application
# /usr/local/bin/python3.13 main.py > /home/oncovue/Downloads/Final_application/autostart.log 2>&1
/usr/bin/python3.13 /home/oncovue/Downloads/Final_application/main.py > /home/oncovue/Downloads/Final_application/autostart.log 2>&1
