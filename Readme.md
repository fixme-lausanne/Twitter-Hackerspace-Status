# Hackerspace

Use by the rfid doorlock (https://fixme.ch/wiki/RFID_Doorlock) to tweet the hackerspace status.
The script is authenticated to twitter using OAuth. It saves the status in a mysql database and a lock file.

The following command are supported:
- ?do=close           Close the space,
- ?do=open            Open the space,
- ?do=custom&hours=x  Open the space for a specific time,
- ?request            Request the state of the hackerspace (open/closed).</pre>";

