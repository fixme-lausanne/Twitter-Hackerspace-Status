#!/usr/bin/python3

#####################################
#   query must be done like this:   #
#   twitter.py?do=open              #
#   twitter.py?do=close             #
#   twitter.py?do=custom&hours=x    #
#####################################

print("Content-type: text/ascii")
print("")

from twitter import Twitter, OAuth
import mysql.connector
import sys, os
import subprocess
import datetime
import cgi
import requests

DEBUG = False

mm_addrs = 'https://chat.fixme.ch'
mm_token = ''
mm_chann = ''

consumer_key = ""
consumer_secret = ""
access_token = ""
access_token_secret = ""

host = "localhost"
database = ""
table = ""
username = ""
password = ""
table = ""

def Usage():
  print("""<pre>USAGE:

  HTTP
  ?do=close           Close the space,
  ?do=open            Open the space,
  ?do=custom&hours=x  Open the space for a specific time,
  ?request            Request the state of the hackerspace (open/closed).</pre>

  CLI
  ./command do hours</pre>\n""")
  sys.exit()

# Generate status
date = datetime.datetime.now().strftime('%d.%m.%Y %H:%M')
form = cgi.FieldStorage()

if DEBUG:
  print('args={}'.format(sys.argv))

if form.getvalue('do') != None:
  do = form.getvalue('do')
  if form.getvalue('hours') != None:
    hours = int(form.getvalue('hours'))
elif len(sys.argv) > 1:
  do = sys.argv[1]
  if len(sys.argv) > 2:
    hours = int(sys.argv[2])
else: 
  Usage()

if DEBUG:
  print('do={}'.format(do))

if do == 'open':
  status = u'The space is open, you are welcome to come over! ({})'.format(date)
elif do == 'close':
  status = 'The space is closed, see you later! ({})'.format(date)
elif do == 'custom':
  status = 'The space is open for {}h, you are welcome to come over! ({})'.format(hours, date)
else:
  Usage()
# TODO: implement state like the perl script ?

# Fortune
motd = subprocess.check_output('/usr/games/fortune -n 200 -s', shell=True)
status += ' ' + motd.decode('utf8')

if DEBUG:
  print('status={}'.format(status))

# Twitter
twit = Twitter(auth=OAuth(access_token, access_token_secret, consumer_key, consumer_secret))
twit.statuses.update(status=status)

# Post to Mastodon
output = subprocess.check_output('/opt/tweet-toot/toot.sh', shell=True)
if DEBUG:
  print('mastodon={}'.format(output))

# Post to Mattermost
status = status.replace('"', '')
status = status.replace("'", '')
status = status.replace('\n', ' ')
req = requests.post('{}/api/v4/posts'.format(mm_addrs), headers={'Authorization': 'Bearer {}'.format(mm_token)}, json={'channel_id': mm_chann, 'message': status})
if DEBUG:
  print('mastodon={}'.format(req.content))

## Post Hackerspace status on website
pub_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
cnx = mysql.connector.connect(user=username, password=password, host=host, database=database)
cursor = cnx.cursor()
if do == 'open':
  cursor.execute('INSERT INTO {} (pub_date, duration, open) VALUES (\'{}\', 0, 1);'.format(table, pub_date))
elif do == 'close':
  cursor.execute('INSERT INTO {} (pub_date, duration, open) VALUES (\'{}\', 0, 0);'.format(table, pub_date))
elif do == 'custom' and hours:
  cursor.execute('INSERT INTO {} (pub_date, duration, open) VALUES (\'{}\', {}, 1);'.format(table, pub_date, hours))
cnx.close()
