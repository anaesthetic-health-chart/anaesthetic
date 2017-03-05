#!/usr/bin/env python

import httplib, urllib
import time
import os.path
import requests
import sys
import time
import urlparse
import json
import requests
import csv

'''
The following is the CSV columns we receive from VSCapture
00 Date
01 Time
02 Heart Rate(/min)
03 Systolic BP(mmHg) - Systolic (Sys) Blood Pressure (BP)
04 Diastolic BP(mmHg) - Diastolic (Dia) BP
05 Mean BP(mmHg)
06 SpO2(%)
07 ETCO2(mmHg) - End Tidal (ET) C02
08 CO2 FI
09 ETO2(mmHg) - End Tidal (ET) C02
10 AA ET - Anaesthetic.Agent (AA) ET
11 AA FI - AA Fraction Inspired (FI)
12 AA MAC SUM - minimum aviolo concentration
13 AA
14 O2 FI
15 N2O FI
16 N2O ET
17 RR - Respiratory Rate (RR)
18 T1 temperature
19 T2
20 P1 HR - (Normally Invasive [P1]) Heart Rate (HR)
21 P1 Sys - P1 Sys BP
22 P1 Dia - P1 Dia BP
23 P1 Mean
24 P2 HR (Central Venous Pressure [P2]) HR
25 P2 Sys
26 P2 Dia
27 P2Mean
28 PPeak - Peak Airway Pressure (PPeak)
29 PPlat - Plateau Pressure (PPlat)
30 TV Exp - Expiratory (Exp) Tidal Volume (TV)
31 TV Insp - Inspiratory (Insp) TV
32 Peep Positive End Expiratory Pressure (Peep)
33 MV Exp minute volume
34 Compliance
35 RR
36 ST II(mm) ecg stuff
37 ST V5(mm)
38 ST aVL(mm)
39 SE state entropy (brain)
40 RE response entropy
41 ENTROPY BSR
42 BIS bispectral index (BWM)
43 BIS BSR
44 BIS EMG
45 BIS SQI
46 **Python mapping of datetime
'''

'''
This is where we map the data from the VSCapture CSV to the data models in
the web app
'''
dataMaps = {
  'Observation': {
    'uri': '/api/v0.1/observation/',
    'map': {
      'bp_systolic': 1,
      'bp_diastolic': 2,
      'pulse': 3,
      'sp02': 4,
      'datetime': 0
    }
  },
  'Gases': {
    'uri': '/api/v0.1/gases/',
    'map': {
        'expired_oxygen': 5,
        'inspired_oxygen': 6,
        'expired_aa': 7,
        'expired_carbon_dioxide': 8,
        'datetime': 0
    }
  },
  'Ventilators': {
    'uri': '/api/v0.1/ventilators/',
    'map': {
      'peak_airway_pressure': 9,
      'peep_airway_pressure': 10,
      'tidal_volume': 11,
      'rate': 12,
      'datetime': 0
    }
  }
}

if len(sys.argv) != 5:
  print "Usage: %s <DATA_CSV> <HEALTH_CHART_BASE_URL> <AUTH_TOKEN>"
  print "  <DATA_CSV> The CSV file with the dummy data (data.csv is included)"
  print "  <HEALTH_CHART_BASE_URL> Base URL of the health chart to send the data to"
  print "           the default is http://127.0.0.1:8000"
  print "  <AUTH_TOKEN> Django Token Auth, Token for REST api"
  print "           to get one use ./manage.py gettoken <username>"
  sys.exit(1)


filename = sys.argv[2]
baseUrl = sys.argv[3]
token = sys.argv[4]
print baseUrl

# Check file exists and open file
if not os.path.isfile(filename):
  print "Couldn't find CSV to read"
  sys.exit(2)

if not sys.argv[4]:
  print "No API token please get one using python manage.py gettoken <username>"
  sys.exit(2)

print "Opening file %s" % filename
fp = open(filename, 'r')

print "What date would you like to use?"
newdate = raw_input('DD/MM/YYYY: ')

newcsv = open('newcsv.csv', 'wb')
writer = csv.writer(newcsv)

#read the first 3 lines then write to new csv
fp.readline()
fp.readline()
fp.readline()

for row in csv.reader(fp):
    date = row[0]
    date2 = newdate + date
    row[0] = date2
    writer.writerow(row)

newcsv.close()
print "date written time to insert"

fp = open('newcsv.csv', 'r')

while 1:
  where = fp.tell()
  line = fp.readline()
  if not line:
    time.sleep(1)
    fp.seek(where)
  else:
    #print line, # already has newline

    parts = line.split(',')

    # Create properly formatted datetime string
    #parts[46] = '%s %s' % (time.strftime('%Y-%m-%d', time.strptime(parts[0], '%d/%m/%Y')), parts[1])
    #parts[46] = '%s %s' % (parts[0], parts[1])

    # Start running maps and POSTs
    for m in dataMaps:
      #print 'Building %s map' % m
      data = {
        'episode_id': 1
      }
      for d in dataMaps[m]['map']:
        if parts[dataMaps[m]['map'][d]] != '-':
          print '%s: %s' % (d, parts[dataMaps[m]['map'][d]])
          data[d] = parts[dataMaps[m]['map'][d]]

      #print 'data is:'
      #print data

      print 'Making url from %s and %s' % (baseUrl, dataMaps[m]['uri'])
      url = urlparse.urljoin(baseUrl, dataMaps[m]['uri'])
      #url = baseUrl + dataMaps[m]['uri']
      print url
      urlBits = urlparse.urlparse(url)

      params = urllib.urlencode({'number': 12524, 'type': 'issue', 'action': 'show'})
      headers = {
        "Content-type": "application/json",
        "Accept": "application/json",
        "Authorization": "Token " + token
      }

      print 'sending ' + json.dumps(data, separators=(',',':'))

      response = requests.post(url, data=json.dumps(data, separators=(',',':')), headers=headers)
      #print response.status, response.reason
