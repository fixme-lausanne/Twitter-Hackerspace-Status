Hackerspace Status
==================

Both scripts use MySQL to put/pull the state of the hackerspace.
The schema can be found in `hackerspace_status.sql`.

Spaceapi.py
-----------
Implements the [Space API](http://spaceapi.net).
- Needs python-mysqldb and python-vobject
- Adds `ext_duration` field, the number of hour(s) the space will be open from `lastchange`
- Uses the [events](https://fixme.ch/civicrm/event/past?html=0&start=20130601&order=1&reset=1)
  in ical format downloaded from a cron

Twitter.pl
----------
Used by the [RFID doorlock](https://fixme.ch/wiki/RFID_Doorlock) and our 
[trigger webapp](trigger.fixme.ch) to tweet the hackerspace status.
The script is authenticated to twitter using `OAuth`. It saves the 
status in a mysql database and a lock file. It does a simple IP check to 
authorize the change of status.

- ?do=close[d]        Close the space,
- ?do=open            Open the space,
- ?do=custom&hours=x  Open the space for a specific amount of time in hour,
- ?request            Request the state of the hackerspace, using the lock file

## Dependencies

 cpan 'install Net::Twitter'
 apt-get install fortune
 pip3 install twitter mysql-python arrow

Drupal
------
Drupal module to show an image in a block of the status from spaceapi.py

