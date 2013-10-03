#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Searches Geolocation of IP addresses using http://freegeoip.net/
It will fetch a csv and return a python dictionary

sample usage:
>>> from freegeoip import get_geodata
>>> get_geodata("189.24.179.76")

{'status': True, 'city': 'Niter\xc3\xb3i', 'countrycode': 'BR', 'ip': '189.24.179.76', 
'zipcode': '', 'longitude': '-43.0944', 'countryname': 'Brazil', 'regioncode': '21', 
'latitude': '-22.8844', 'regionname': 'Rio de Janeiro'}
"""

from urllib import urlopen
from csv import reader
import sys
import re

__author__="Victor Fontes Costa"
__copyright__ = "Copyright (c) 2010, Victor Fontes - victorfontes.com"
__license__ = "GPL"
__version__ = "2.1"
__maintainer__ = __author__
__email__ = "contato [a] victorfontes.com"
__status__ = "Development"

FREE_GEOIP_CSV_URL = "http://freegeoip.net/csv/%s"


def valid_ip(ip):

    pattern = r"\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b"

    return re.match(pattern, ip)

def __get_geodata_csv(ip):
    if not valid_ip(ip):
        raise Exception('Invalid IP format', 'You must enter a valid ip format: X.X.X.X')

    URL = FREE_GEOIP_CSV_URL % ip
    response_csv = reader(urlopen(URL))
    csv_data = response_csv.next()

    return {
        "status": u"True" == csv_data[0],
        "ip":csv_data[1],
        "countrycode":csv_data[2],
        "countryname":csv_data[3],
        "regioncode":csv_data[4],
        "regionname":csv_data[5],
        "city":csv_data[6],
        "zipcode":csv_data[7],
        "latitude":csv_data[8],
        "longitude":csv_data[9]
    }

def get_geodata(ip):
    return __get_geodata_csv(ip)

if __name__ == "__main__":     #code to execute if called from command-line
    intput_ip = sys.argv[1]
    geodata = get_geodata(intput_ip)
    print "IP: %s" % geodata["ip"]
    print "Country Code: %s" % geodata["countrycode"]
    print "Country Name: %s" % geodata["countryname"]
    print "Region Code: %s" % geodata["regioncode"]
    print "Region Name: %s" % geodata["regionname"]
    print "City: %s" % geodata["city"]
    print "Zip Code: %s" % geodata["zipcode"]
    print "Latitude: %s" % geodata["latitude"]
    print "Longitude: %s" % geodata["longitude"] 