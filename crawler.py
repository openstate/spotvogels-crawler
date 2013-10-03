#!/usr/bin/env python

import sys
import os
import re
import json

from pprint import pprint
from time import sleep

import MySQLdb

import requests

def get_prids():
    conn = MySQLdb.connect(
        host='localhost',
        user='spotvogel',
        passwd='spotvogel',
        db='spotvogel'
    )
    cursor = conn.cursor()
    cursor.execute("""SELECT prid FROM Video WHERE prid IS NOT NULL""")
    return [r[0] for r in cursor.fetchall() if re.search('^VARA_', r[0])]

def main():
    prids = get_prids()
    videos = []
    for prid in prids:
        contents = requests.get(u'http://e.omroep.nl/metadata/aflevering/%s' % (prid,)).text
        video = json.loads(contents[14:-2]) # cuts of a function call
        videos.append(video)
        sleep(1)
    print json.dumps(videos)
    return 0

if __name__ == '__main__':
    sys.exit(main())