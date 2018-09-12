#!/usr/bin/env python3

import os
import datetime
import pytz
import json
import xml.etree.cElementTree as ET
import requests
import urllib.parse

# *** CONFIGURATION ***
with open('/opt/sundtek-to-xmltv/config.json', 'r') as f:
    config = json.load(f)

# URL to servercmd.xhx
SERVERCMD = 'http://{0}:{1}/servercmd.xhx'.format(config['SERVER']['IP'],
                                                  config['SERVER']['PORT'])
# How many days to fetch (including today)? Set to 0 to only fetch data from `now`.
# Beware that a couple days can already take a couple minutes, even with just 20 channels.
DAYS = config['FETCH']['DAYS']
# Which Channel groups should be parsed?
# If the array is empty, each channel whould be fetched.
# e.g. CHANNEL_GROUPS = '[\"FreeTV\"]'
CHANNEL_GROUPS = config['FETCH']['CHANNEL_GROUPS']
# Where to save the output (relative save filepath).
RELATIVE_FILE_PATH = config['RESULT']['FILE_PATH']
# enable/disable DEBUG print
DEBUG = config['RESULT']['DEBUG_OUTPUT']
# *** CONFIGURATION END ***

def debug_print(text):
    if DEBUG:
        print(text)

def get_readable_days(days):
      if days == 0:
          return 'now'
      else:
          return days + ' day\s'

def get_readable_channel_group_names(channels_groups):
    if len(channels_groups) > 0:
        return "channel group\s {0}".format(
                ', '.join(channels_groups))
    else:
        return "all channels"

debug_print("grab data for {0} from {1} for {2} and save to {3}".format(
    get_readable_channel_group_names(CHANNEL_GROUPS),
    SERVERCMD,
    get_readable_days(DAYS),
    RELATIVE_FILE_PATH))

# Fetch overview
def fetch_overviews_for_days(days):
    result = []
    if days == 0:
        # Fetch data for Now
        debug_print("data for now would be fetched")
        r = requests.post(SERVERCMD,
                          data={
                              'epgmode': 'now',
                              'epgfilter': 'now',
                              'groups': CHANNEL_GROUPS
                          })
        result.append(r.json())
    else:
        # Fetch data for x days
        for offset in range(days):
            date = datetime.date.today() + datetime.timedelta(days=offset)
            debug_print("data for Day " + str(date) + " would be fetched")
            r = requests.post(SERVERCMD,
                              data={
                                  'epgmode': 'calendar',
                                  'date': str(date),
                                  'groups': CHANNEL_GROUPS,
                              })
            result.append(r.json())
    return result


def format_time(timestamp):
    dt = pytz.utc.localize(datetime.datetime.utcfromtimestamp(timestamp))
    return dt.strftime('%Y%m%d%H%M%S %Z')


# Get show details
def get_show_data(service_id, event_id, delsys):
    r = requests.post(SERVERCMD,
                      data={
                          'epgserviceid': service_id,
                          'epgeventid': event_id,
                          'delsys': delsys,
                          'groups': CHANNEL_GROUPS,
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
def parse_channels_shows(overviews):
    global channels
    global shows
    for overview_index, overview in enumerate(overviews):
        debug_print("parse overview " + str(overview_index))
        for channel_index, channel in enumerate(overview):
            debug_print("parse channel " + str(channel_index) + " - " + channel[1])
            service_id = channel[2]
            delsys = channel[3]
            if service_id not in channels:
                name = channel[1]
                channels[service_id] = {
                    'name': name,
                    'delsys': delsys,
                }
            for show_index, show in enumerate(channel[4:]):
                debug_print("parse show " + str(show_index) + " of channel " + channel[1])
                event_id = show[2]
                if event_id not in shows:
                    shows[event_id] = get_show_data(service_id, event_id, delsys)


# Generate XML content
def generate_xml_content(channels, shows):
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
    return tree


# Write out data
def save_xml_file(path, xml_tree):
    with open(path, 'wb') as fh:
        fh.write('''<?xml version="1.0" encoding="utf-8"?>
    <!DOCTYPE tv SYSTEM "xmltv.dtd">'''.encode('utf-8'))
        xml_tree.write(fh, 'utf-8')


# main execution
overviews = fetch_overviews_for_days(DAYS)
channels = {}
shows = {}
parse_channels_shows(overviews)
tree = generate_xml_content(channels, shows)
save_xml_file(os.path.join(os.path.dirname(os.path.realpath(__file__)),
              RELATIVE_FILE_PATH), tree)
