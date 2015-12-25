#!/usr/bin/python
#
# echo local NMEA data in csv

import socket
import pynmea2
import os

# listen to NMEA data 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('',10110))
r = pynmea2.NMEAStreamReader(s.makefile())

devname = "/dev/airmar200wx"
try:
    os.makedirs(devname)
except OSError:
    if not os.path.isdir(devname):
        raise

while True:
    for msg in r.next():
#        print msg; continue
        if isinstance(msg, pynmea2.types.MDA):
            print msg
            print "Barometric pressure (mbar):", msg.b_presure_bar*1000
            print "Air temperature (*C):", msg.air_temp
            print "Water temperature (*C):", msg.water_temp
            print "Relative humidity (%):", msg.rel_humidity
            print "Absolute humidity (%):", msg.abs_humidity
            print "Dew point (*C):", msg.dew_point
            print "Wind direction (deg E of TN):", msg.direction_true
            print "Wind direction (deg E of MN):", msg.direction_magnetic
            print "Wind speed (m/s):", msg.wind_speed_meters
            print

            translations = (
                ('barometric_pressure', msg.b_presure_bar*1000),
                ('air_temperature', msg.air_temp),
                ('relative_humidity', msg.rel_humidity),
                ('dew_point_temperature', msg.dew_point),
                ('wind_direction_true', msg.direction_true),
                ('wind_direction_magnetic', msg.direction_magnetic),
                ('wind_speed', msg.wind_speed_meters)
                )
            for (devfile, data) in translations:
                with open(os.path.join(devname, devfile), 'w') as outfile:
                    #outfile.write(str(getattr(msg, 'air_temp')))
                    outfile.write(str(data))


        # sentences possibly transmitted by 200WX
        #
        # GPDTM - Datum Reference
        # GPGGA - Global Positioning System Fix Data
        # GPGLL - Geographic Position, Latitude and Longitude
        # GPGSA - GPS DOP and Active Satellites
        # GPGSV - GPS Satellites in View
        # HCHDG - Heading, Deviation and Variation
        # HCHDT - Heading
        # WIMDA - Meteorological Composite
        # WIMWD - Wind Direction
        # WIMWV - Wind Speed and Angle
        # GPRMC - Recommended minimum specific GPS/Transit data
        # TIROT - Rate of Turn
        # GPVTG - Track Made Good and Ground Speed
        # WIVWR - Relative Wind Speed and Angle
        # WIVWT - True Wind Speed and Angle
        # YXXDR - Transducer data
        # GPZDA - Date and Time



