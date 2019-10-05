#!/usr/bin/env python3
# pylint: disable=invalid-name
'''Log data from a Solis 4G inverter every 60 seconds, writing to a CSV file'''

import csv
import logging
import os
import time
from datetime import datetime
import requests

def log_entry(url, output):
    '''Function to retrieve and log data from inverter'''
    try:
        r = requests.get(url).json()
    except requests.exceptions.ConnectionError:
        return
    with open(output, 'a') as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow([datetime.now().strftime('%c'),
                            r['i_pow_n'],
                            float(r['i_eday'])])

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    if 'INVERTER_IP' not in os.environ or 'OUTPUT' not in os.environ:
        logging.fatal("INVERTER_IP and OUTPUT environment variables must be set")
        exit(-1)

    inverter_url = 'http://{}/status.json?CMD=inv_query'.format(os.environ['INVERTER_IP'])

    while True:
        # Try to always log data at the top of the minute. Also avoids spamming
        # the inverter with requests if it
        time.sleep(60 - datetime.now().second)
        log_entry(inverter_url, os.environ['OUTPUT'])
