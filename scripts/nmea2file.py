#!/usr/bin/python
#
# echo local NMEA data in csv

import socket
import os

import logging
from logging.handlers import TimedRotatingFileHandler

print "starting nmea2file.py"

# listen to NMEA data 
kplex = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
kplex.connect(('',10110))
nmea_port = kplex.makefile()

print "connected to kplex"

logfile = TimedRotatingFileHandler('/var/log/airmar200wx/nmea/nmea',
        when='midnight', interval=1, backupCount=365)
logfile.setFormatter(logging.Formatter('%(message)s'))

logger = logging.getLogger('airmar200wx.nmea')
logger.setLevel(logging.INFO)
logger.addHandler(logfile)

print "done with logging stuff"

while True:
    try:
        msg = nmea_port.readline()
        logger.info(msg.rstrip())
    except (KeyboardInterrupt, SystemExit):
        # effbot.org/zone/stupid-exceptions-keyboardinterrupt.htm
        raise
    except:
        print "exception occured! continuing..."
        continue
