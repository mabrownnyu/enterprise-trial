'''
Megan Brown

Collect Tweets from the enterprise API
'''
import argparse
import datetime
import json
import os
import ssl
import sys

import requests

# Argparse for cli options. Run `python engagement_totals.py -h` to see list of available arguments.
parser = argparse.ArgumentParser()
parser.add_argument("-c", "--chunksize", type=int, help="Overrides default chunksize of '10000'.")
args = parser.parse_args()

USERNAME = os.environ.get('USERNAME')
PASSWORD = os.environ.get('PASSWORD')

endpoint = 'https://gnip-stream.twitter.com/stream/powertrack/accounts/NYUCenterForSocialMediaAndPolitics/publishers/twitter/dev.json'

headers = {
    'connection': "keep-alive",
    'accept': 'application/json',
    'Accept-Encoding': 'gzip',
    'gnipkeepalive': '30',
}


def main():
    if args.chunksize:
        chunksize = args.chunksize
    else:
        chunksize = 10000
    try:
        get_stream(endpoint, chunksize)
    except ssl.SSLError as e:
        sys.stderr.write(f"Connection failed: {e}\n")


def get_stream(endpoint, chunksize):
    response = requests.get(url=endpoint, auth=(USERNAME, PASSWORD), stream=True, headers=headers)
    print('STATUS CODE', response.status_code)
    while True:
        for chunk in response.iter_content(chunksize, decode_unicode=True):  # Content gets decoded
            chunk = chunk.strip()

            if chunk:
                try:
                    # load the data
                    data = json.loads(chunk)
                    
                    # figure out where to output the data
                    time = datetime.datetime.now()
                    year = time.year
                    month = '{:02d}'.format(time.month)
                    day = '{:02d}'.format(time.day)

                    out_file = f'/mnt/{year}_{month}_{day}__election_tweets.json'
                    
                    # output the data
                    with open(out_file, 'a+') as op:
                        op.write(json.dumps(data) + '\n')

                except:
                    print("Could not resolve", chunk)

            else:
                print("Waiting for data....", str(datetime.datetime.now()))

if __name__ == '__main__':
    main()