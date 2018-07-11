#!/usr/bin/env python3

import os
import datetime
import xml.etree.cElementTree as ET

import requests
import urllib.parse

# *** CONFIGURATION ***
# URL to servercmd.xhx
SERVERCMD = 'http://localhost:22000/servercmd.xhx'
# How many days do we fetch data for (including today)? Set to None to only
# fetch data from `now`. Beware that a couple days can already take a couple
# minutes, even with just 20 channels.
CALENDAR = 3
# Where to save the XML file to
XML_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)),
                        'epg.xml')


# Fetch overview
data = []
# Now
r = requests.post(SERVERCMD,
                  data={
                      'epgmode': 'now',
                      'epgfilter': 'now',
                      'groups': '[]',
                      'channels': '1,2,3,4,5'
                  })
data.append(r.json())
# Calendar
for offset in range(CALENDAR):
    date = datetime.date.today() + datetime.timedelta(days=offset)
    r = requests.post(SERVERCMD,
                      data={
                          'epgmode': 'calendar',
                          'date': str(date),
                          'groups': '[]',
                      })
    data.append(r.json())


def format_time(timestamp):
    dt = datetime.datetime.utcfromtimestamp(timestamp).astimezone(None)
    return dt.strftime('%Y%m%d%H%M%S %Z')


def show_data(service_id, event_id, delsys):
    r = requests.post(SERVERCMD,
                      data={
                          'epgserviceid': service_id,
                          'epgeventid': event_id,
                          'delsys': delsys,
                      })
    data = r.json()
    details = data[3]
    start = format_time(details[0])
    stop = format_time(details[0] + details[1])
    event_id = details[2]
    title = urllib.parse.unquote(details[3])
    desc = urllib.parse.unquote(details[5])
    return {
        'service_id': service_id,
        'start': start,
        'stop': stop,
        'title': title,
        'desc': desc,
    }


# Parse data
channels = {}
shows = {}
for data_ in data:
    for channel in data_:
        service_id = channel[2]
        delsys = channel[3]
        if service_id not in channels:
            name = channel[1]
            channels[service_id] = {
                'name': name,
                'delsys': delsys,
            }
        for show in channel[4:]:
            event_id = show[2]
            if event_id not in shows:
                shows[event_id] = show_data(service_id, event_id, delsys)

# Generate XML
tv = ET.Element('tv', attrib={'generator-info-name': 'Sundtek EPG Parser/0.1'})
for service_id, channel in channels.items():
    el = ET.SubElement(tv, 'channel', id=service_id)
    ET.SubElement(el, 'display-name').text = channel['name']
for event_id, show in shows.items():
    programme = ET.SubElement(tv, 'programme', start=show['start'],
                              stop=show['stop'], channel=show['service_id'])
    ET.SubElement(programme, 'title', lang='de').text = show['title']
    ET.SubElement(programme, 'desc', lang='de').text = show['desc']
tree = ET.ElementTree(tv)

# Write out data
with open(XML_PATH, 'wb') as fh:
    fh.write('''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE tv SYSTEM "xmltv.dtd">'''.encode('utf-8'))
    tree.write(fh, 'utf-8')
