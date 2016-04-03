#!/usr/bin/python
#
# update scadabr with latest value; use cron to run minutely
#
# Patrick O'Keeffe

import urllib2
import subprocess
from datetime import datetime

reporturl = 'http://10.1.1.3/ScadaBR/httpds?'
deviceid = '__device=weather'
#timestamp = datetime.now().strftime('__time=%Y%m%d%H%M00')

datafile = '/var/log/airmar200wx/1hz/weather'
last_record = subprocess.check_output(['tail', '-n', '1', datafile]).strip()
(ts, p_baro, t_air, rh, t_dew, wd_true, wd_mag, ws) = last_record.split('\t')

timestamp = datetime.strptime(ts, '%Y-%m-%d %H:%M:%S').strftime('__time=%Y%m%d%H%M00')

vals = ['wx_p_baro=%s' % p_baro, 'wx_t_air=%s' % t_air, 'wx_rh=%s' % rh,
        'wx_t_dew=%s' % t_dew, 'wx_wd_true=%s' % wd_true, 'wx_ws=%s' % ws]

urllib2.urlopen(reporturl + '&'.join([deviceid, timestamp]+vals))
