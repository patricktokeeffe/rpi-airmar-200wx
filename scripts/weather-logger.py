#!/usr/bin/python
#
# echo local NMEA data in csv

import socket
import os

import logging
from logging.handlers import TimedRotatingFileHandler

# listen to NMEA data 
kplex = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
kplex.connect(('',10110))
nmea_port = kplex.makefile()

logfile = TimedRotatingFileHandler('/var/log/airmar200wx/tsv/weather',
        when='midnight', interval=1, backupCount=365)
logfile.suffix = '%Y-%m-%d.tsv'
logfile.setFormatter(logging.Formatter('%(asctime)s\t%(message)s', datefmt='%Y-%m-%d %H:%M:%S'))

logger = logging.getLogger('airmar200wx.nmea.wimda')
logger.setLevel(logging.INFO)
logger.addHandler(logfile)

while True:
    try:
        msg = nmea_port.readline()
        if msg.startswith('$WIMDA'):

            (_,_,_,P_baro,_,T_air,_,_,_,RH,_,T_dew,_,WD_true,_,WD_mag,_,_,_,WS,_) = msg.split(',')
            P_baro = str(1000*float(P_baro)) #bar -> mbar
            logger.info('\t'.join([P_baro, T_air, RH, T_dew, WD_true, WD_mag, WS]))
    except (KeyboardInterrupt, SystemExit):
        # effbot.org/zone/stupid-exceptions-keyboardinterrupt.htm
        raise
    except:
        continue
