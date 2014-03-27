#!/usr/bin/env python
# -*- coding: utf8 -*-

import cgitb, json, MySQLdb, sys, time
from datetime import datetime
import vobject
from pprint import pprint

cgitb.enable()
print 'Content-Type: application/json'
#print 'Access-Control-Allow-Origin: *' #Provide this server side or in this script
#print 'Cache-Control: no-cache'
print

#
# Default description of the Space API
#
api = {
  'api':      '0.13',
  'space':    'FIXME',
  'logo':     'https://fixme.ch/sites/default/files/Logo5_v3-mini.png',
  'url':      'https://fixme.ch',
  'contact':  {
                'phone':      '+41216220734',
                'keymaster':  ['+41797440880'],
                'irc':        'irc://freenode/#fixme',
                'twitter':    '@_fixme',
                'email':      'info@fixme.ch',
                'ml':         'hackerspace-lausanne@lists.saitis.net',
                'facebook':   'https://www.facebook.com/fixmehackerspace',
                'wiki':       'https://wiki.fixme.ch',
              },
  'location': {
                'lon':  6.613828,
                'lat':  46.524652,
                'address':  'Rue de Genève 79, 1004 Lausanne, Switzerland',
              },
  'state':    {
                'icon':     {
                  'open': 'https://fixme.ch/sites/default/files/logo-open.png',
                  'closed': 'https://fixme.ch/sites/default/files/logo-closed.png',
                },
                'ext_duration': 0, # Custom field for the open duration
              },
  'events':   [],
  'feeds':    {
                'blog': {'type': 'rss', 'url': 'https://fixme.ch/rss.xml'},
                'wiki': {'type': 'rss', 'url': 'https://fixme.ch/w/index.php?title=Special:RecentChanges&feed=atom'},
                'calendar': {'type': 'ical','url': 'https://www.google.com/calendar/ical/sruulkb8vh28dim9bcth8emdm4%40group.calendar.google.com/public/basic.ics'},
              },
  'stream':   {
                'mjpeg': 'http://62.220.135.212/mjpg/video.mjpg',
                'html': 'http://webcam.fixme.ch',
              },
  'issue_report_channels': ['email', 'twitter'],
  'sensors': {
                'people_now_present': [{
                  'value':        0,
                  'unit':         'device(s)',
                  'description':  'Number of devices on the network (excluding some devices)',
                }],
                'total_member_count': [
                  {
                    'value': 21, #2014-03-27
                    'unit': 'premium members',
                  },
                  {
                    'value': 45, #2014-03-27
                    'unit': 'standard members',
                  },
                ],
             }
}

#
# Get sensors data
#
try:
    user_online = int(open('/var/log/user_online.log', 'r').read())
except:
    user_online = 0

if user_online > 0:
    api['sensors']['people_now_present'][0]['value'] = user_online

#
# Get last 10 events
#
try:
    ical = vobject.readOne(open('./civicrm_ical.ics', 'r').read())
    for e in ical.vevent_list[:10]:
        ts = int(time.mktime(e.dtstart.value.timetuple()))
        api['events'].append({
            'name': e.summary.value,
            'type': e.categories.value[0],
            'timestamp': ts,
            't':    ts,
        })
except IOError,e:
    print e

#
# Get Open/Close status
#
try:
    db = MySQLdb.connect(host="localhost", user="***REMOVED***", passwd="***REMOVED***", db="hackerspace_status")
    c = db.cursor()
    c.execute('select pub_date, duration, open from hackerspace_status order by id desc limit 1;')
    result = c.fetchone()
    db.close()
except Exception,e:
    result = None

if result != None and len(result) == 3:
    res_date = result[0]
    res_duration = result[1]
    res_open = result[2]
else:
    res_date = datetime.now()
    res_duration = 0
    res_open = False

#
# Update API
#
api['state']['open'] = bool(res_open)
api['state']['lastchange'] = time.mktime(res_date.timetuple())
api['state']['ext_duration'] = int(res_duration)
diff = datetime.now() - res_date
if res_open == True and diff.seconds / 3600 >= res_duration:
    api['state']['message'] = 'The space may be closed, the initial duration of %i hour(s) is exceeded.'  % res_duration
elif res_open == True:
    api['state']['message'] = 'The space is open.'
else:
    api['state']['message'] = 'The space is closed.'

#
# Pretty print JSON
#
print json.dumps(api)
