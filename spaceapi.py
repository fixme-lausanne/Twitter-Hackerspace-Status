#!/usr/bin/env python
# -*- coding: utf8 -*-

import cgitb, json, MySQLdb, sys, time
from datetime import datetime
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
  'api':      '0.12',
  'space':    'FIXME',
  'logo':     'https://fixme.ch/sites/default/files/Logo5_v3-mini.png',
  'icon':     {
                'open': 'https://fixme.ch/sites/default/files/logo-open.png',
                'closed': 'https://fixme.ch/sites/default/files/logo-closed.png',
              },
  'url':      'https://fixme.ch',
  'address':  'Rue de Genève 79, 1004 Lausanne, Switzerland',
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
  'lon':      6.613828,
  'lat':      46.524652,
  'open':     False,
  'duration': 0, # Custom field for the open duration
  'status':   '',
  'lastchange': 0,
  'events':   ['https://fixme.ch/civicrm/event/past?html=1&start=20101201&order=1&reset=1'],
  'feeds':    [
                {'name': 'site', 'type': 'application/rss+xml', 'url': 'https://fixme.ch/rss.xml'},
                {'name': 'wiki', 'type': 'application/rss+xml', 'url': 'https://fixme.ch/w/index.php?title=Special:RecentChanges&feed=atom'},
                {'name': 'calendar', 'type': 'text/calendar','url': 'https://www.google.com/calendar/ical/sruulkb8vh28dim9bcth8emdm4%40group.calendar.google.com/public/basic.ics'},
              ],
}

#
# Get Open/Close status
#
try:
    db = MySQLdb.connect(host="localhost", user="hs_status", passwd="r3fG!yNx", db="hackerspace_status")
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
api['lastchange'] = time.mktime(res_date.timetuple());
api['open'] = bool(res_open)
api['duration'] = int(res_duration)
diff = datetime.now() - res_date
if res_open == True and diff.seconds / 3600 >= res_duration:
  api['status'] = 'The space may be closed, the initial duration of %i hour(s) is exceeded.'  % res_duration
elif res_open == True:
  api['status'] = 'The space is open.'
else:
  api['status'] = 'The space is closed.'

#
# Pretty print JSON
#
print json.dumps(api)
