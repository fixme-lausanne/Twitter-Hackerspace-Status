#!/usr/bin/env python
# -*- coding: utf8 -*-

import cgitb, json, MySQLdb, sys, time
from datetime import datetime
import vobject
from pprint import pprint
import requests

cgitb.enable()
print 'Content-Type: application/json'
#print 'Access-Control-Allow-Origin: *' #Provide this server side or in this script
#print 'Cache-Control: no-cache'
print

# Power Consumption
power_consumption = []
flusko_uri = 'http://192.168.130.129:8080/sensor/{}?version=1.0&interval=minute&unit=watt'
clamps_id = [
    '34cde81adabfb1ce819eca8fea6949b6',
    'b7755b5f3ec05fcdc67f449241a9912a',
    'e67e0685f747b30d855108ab781abdfc',
]

i = 1
for clamp in clamps_id:
    req = requests.get(flusko_uri.format(clamp))
    data = req.json()
    power_consumption.append({
        'value':        data[0][1],
        'unit':         'W',
        'location':     'fixme',
        'name':         'L' + str(i),
    })
    i += 1

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
                'chat':       'https://chat.fixme.ch',
              },
  'location': {
                'lon':  6.591292,
                'lat':  46.532372,
                'address':  'Chemin du Closel 3, 1020 Renens, Switzerland',
              },
  'state':    {
                'icon':     {
                  'open': 'https://fixme.ch/sites/default/files/logo-open.png',
                  'closed': 'https://fixme.ch/sites/default/files/logo-closed.png',
                },
                'ext_duration': 0, # Custom field for the open duration
              },
  #'events':   [],
  'feeds':    {
                'blog': {'type': 'rss', 'url': 'https://fixme.ch/rss.xml'},
                'wiki': {'type': 'rss', 'url': 'https://fixme.ch/w/index.php?title=Special:RecentChanges&feed=atom'},
                'calendar': {'type': 'ical','url': 'https://www.google.com/calendar/ical/sruulkb8vh28dim9bcth8emdm4%40group.calendar.google.com/public/basic.ics'},
              },
  #'stream':   {
  #              'html': 'http://webcam.fixme.ch',
  #            },
  'issue_report_channels': ['email', 'twitter'],
  'sensors': {
                #'temperature': [
                #    {
                #        'value': 0,
                #        'unit': '°C',
                #        'location': 'Bitcoin farm',
                #    },
                #    {
                #        'value': 0,
                #        'unit': '°C',
                #        'location': 'Room',
                #    }
                #],
                'people_now_present': [{
                  'value':        0,
                  'unit':         'device(s)',
                  'description':  'Number of devices in the DHCP range',
                }],
                'power_consumption': power_consumption,
                'total_member_count': [ #2019-10-12
                  {
                    'value': 28,
                    'unit': 'premium members',
                  },
                  {
                    'value': 50,
                    'unit': 'standard members',
                  },
                  {
                    'value': 78,
                    'unit': 'total members',
                  },
                ],
             }
}

#
# Get sensors data
#

# People
user_online = 0
try:
    user_online = int(open('/var/log/user_online.log', 'r').read())
except:
    pass

if user_online > 0:
    api['sensors']['people_now_present'][0]['value'] = user_online

# Temp
nb_temp = 2
temp = 0.0
for i in xrange(nb_temp):
    try:
        temp = open('/var/log/temp_%d.log' % (i+1), 'r').read()
        if temp != '':
            api['sensors']['temperature'][i]['value'] = float(temp)
    except:
        pass

#
# Get last 10 events
#
#try:
#    ical = vobject.readOne(open('./civicrm_ical.ics', 'r').read())
#    for e in ical.vevent_list[:10]:
#        ts = int(time.mktime(e.dtstart.value.timetuple()))
#        api['events'].append({
#            'name': e.summary.value,
#            'type': e.categories.value[0],
#            'timestamp': ts,
#            't':    ts,
#        })
#except Exception,e:
#    pass

#
# Get Open/Close status
#
try:
    db = MySQLdb.connect(host="", user="", passwd="", db="")
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
