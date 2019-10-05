# Solis 4G inverter logging

We have recently had a solar system installed, which (briefly) consists of some
solar panels, an inverter to convert the DC output to mains AC and a bunch of cabling
and meters. Unfortuantely, although we have a total power generated meter there's no
easy way to get a graph from the very simple API allowing you to optimise power usage,
i.e. run washing machines, dishwashers and other appliances during peak power generation.

## Overview

This script downloads data from the provided web interface. Rather than requiring some
ugly scraping, the inverter has a nice endpoint which returns all the data we need in a
JSON format. (If the authors of the inverter software are reading this: Thanks, I wish
more people would do this rather than generating static web pages on the fly)

You'll probably want do give your inverter a static IP so you can reliably
find it on the network, but once you have, it's easy to get the data:

    $ curl http://192.168.0.8/status.json?CMD=inv_query
    {"g_sn":190527XXXX,"g_ver":"ME-121001-V1.0.6(201704012008)","time":1570258745,
     "g_time":1874,"g_err":0,"mac":"98-d8-63-53-XX-XX","auto_ip":0,"ip":"192.168.0.8",
      "sub":"255.255.255.0","gate":"192.168.0.1","auto_dns":0,"dns":"208.67.222.222",
      "dns_bak":"208.67.222.222","i_status":16,"i_type":1283,"i_num":1,
      "i_sn":"160E71194180XXXX","i_ver_m":"","i_ver_s":"","i_modle":"","i_pow":"",
      "i_pow_n":141,"i_eday":"0.0","i_eall":"6.0","i_alarm":"F22F23","i_last_t":0,
      "l_a_agr":0,"l_a_ip":"XX.XX.XX.XX","l_a_port":XXXXX}

(Line breaks added to the above for readability, you can pipe through jq if you want
something more readable than just a blob of JSON)

Of the fields availablem the ones of most interest to us as `i_pow_n`, current power
generation in Watts, and `i_eall`, total power generated today in kilowatt hours.

## Getting and running the code

To download and run the script from the Unix or OS X command line: (This assumes
you already have `git`, `python3` and the Python 3 module `requests` installed)

    git clone git@github.com:zoeimogen/SolarLog.git
    cd SolarLog
    INVERTER_IP=192.168.0.8 OUTPUT=solar.csv ./solarlog.py

The output file should be readable by anything that understand CSV, and consists of
the time (UTC), current generation in Watts and total daily generation in kWh:

    $ tail -5 solar.csv 
    Fri Oct  4 17:53:00 2019,163,6.2
    Fri Oct  4 17:54:00 2019,164,6.2
    Fri Oct  4 17:55:01 2019,165,6.2
    Fri Oct  4 17:56:00 2019,165,6.2
    Fri Oct  4 17:57:00 2019,166,6.2

There is a simple guide on how to run a Python script on boot as a system service in
Linux at https://www.raspberrypi-spy.co.uk/2015/10/how-to-autorun-a-python-script-on-boot-using-systemd/.
Because I have quite a few of these scripts, I run them in Docker which saves messing
about with dependencies:

    docker build . -t solarlog
    docker run -e OUTPUT=/output/solar.csv -e INVERTER_IP=192.168.0.8 --init -d \
        --name="solarlog" --restart always -v /home/zoe/SolarLog:/output solarlog:latest

The `-v` mounts a directory on your local machine from within Docker, so in this example
the output file will be in `home/zoe/SolarLog`.

It should work on Windows too, but as I don't have a machine to test on you're on
your own.