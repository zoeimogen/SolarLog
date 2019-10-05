#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=invalid-name

import requests
import json
import csv
import logging
import os
import time
from datetime import datetime

def log_entry():
    try:
        r = requests.get('http://192.168.0.8/status.json?CMD=inv_query').json()
    except requests.exceptions.ConnectionError:
        return
    f = open(os.environ['OUTPUT'], 'a', buffering=1)
    csvwriter = csv.writer(f)
    csvwriter.writerow([datetime.now().strftime('%c'),
                        r['i_pow_n'],
                        float(r['i_eday'])])

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    while True:
        time.sleep(60 - datetime.now().second)
        log_entry()
