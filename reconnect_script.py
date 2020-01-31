'''
Megan Brown

Restart stopped Tweets if the file has not been written to in a while
'''
import datetime
import os

import collect_tweets

USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')

endpoint = 'https://gnip-stream.twitter.com/stream/powertrack/accounts/NYUCenterForSocialMediaAndPolitics/publishers/twitter/dev.json'

headers = {
    'connection': "keep-alive",
    'accept': 'application/json',
    'Accept-Encoding': 'gzip',
    'gnipkeepalive': '30',
}

time = datetime.datetime.now()
year = time.year
month = '{:02d}'.format(time.month)
day = '{:02d}'.format(time.day)

out_file = f'/mnt/{year}_{month}_{day}__election_tweets.json'

mtime = os.path.getmtime(out_file)
last_mtime = datetime.datetime.utcfromtimestamp(mtime)

print("CURRENT TIME:", time, "LAST UPDATE:", last_mtime)

time_delt = datetime.timedelta(minutes=15)
if time - last_mtime > time_delt:
    print("YIKES IT STOPPED")


    collect_tweets.main()