Hackerspace Status
==================

Both scripts use MySQL to put/pull the state of the hackerspace. The schema can be found in `hackerspace_status.sql`.

Spaceapi.py
-----------
Implements the Space API from [hackerspaces.nl](https://hackerspaces.nl/spaceapi/).

- Add `duration` field, the number of hour(s) the space will be open from `lastchange`

Twitter.pl
----------
Use by the [RFID doorlock](https://fixme.ch/wiki/RFID_Doorlock) to tweet the hackerspace status.
The script is authenticated to twitter using `OAuth`. It saves the status in a mysql database and a lock file.
It does a simple IP check to authorize the change of status.

- ?do=close[d]        Close the space,
- ?do=open            Open the space,
- ?do=custom&hours=x  Open the space for a specific amount of time in hour,
- ?request            Request the state of the hackerspace, using the lock file
