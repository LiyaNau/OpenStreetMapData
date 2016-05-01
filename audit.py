#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
import codecs
import sys

OSMFILE = "saint-petersburg_russia.osm"
street_type_re = re.compile(ur'\b[а-я][а-яА-ЯЁё-]+\.?', re.U,)
postcode_re = re.compile(ur'^1[89][0-9]{4}', re.U)


expected = [u"улица", u"проспект", u"бульвар", u"проезд", u"набережная", u"переулок", u"площадь", u"линия", u"шоссе", 
            u"канал", u"остров", u"вал", u"тупик", u"пост", u"дорога", u"аллея", u"посёлок", u"парк", u"проток",
             u"садоводство", u"тракт", u"бор", u"холмы", u"деревня", u"квартал", u"крепость", u"территория", u"горка", u"городок"]
problem = [u"ул." , u"пр.", u"пер.", u"бул.", u"наб.", u"пл."]


mapping = { u"St": "Street",
            "St.": "Street",
            "Ave": "Avenue",
            "Rd.": "Road"
            }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(unicode(street_name))
    if m:
        street_type = m.group()
        #print repr(m.group()).decode('unicode-escape')
        #print m.group()
        if street_type not in expected:
            print street_type
            street_types[street_type].add(street_name)
        if street_type in problem:
            print street_type


def audit_postcode(postcodes, code):
    m = postcode_re.match(unicode(code))
    if not m:
        postcodes.add(code)




def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def is_city_name(elem):
    return (elem.attrib['k'] == "addr:city")


def is_postcode(elem):
    return (elem.attrib['k'] == "postal_code" or elem.attrib['k'] == "addr:postcode")


def audit(osmfile):
    osm_file = codecs.open(osmfile, "rb",encoding = 'utf-8')
    street_types = defaultdict(set)
    cities = set()
    postcodes = set()
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    #k = tag.attrib['v']
                    #print repr(k).decode('unicode-escape')
                    #print tag.attrib['v'].encode('utf-8','replace')
                    #pprint.pprint(tag.attrib['v'].encode('cp1251'))
                    #print repr(tag.attrib['v']).decode('unicode-escape')
                    audit_street_type(street_types, tag.attrib['v'])

                if is_city_name(tag):
                    cities.add(tag.attrib['v'])
                if is_postcode(tag):
                    audit_postcode(postcodes, tag.attrib['v'])


    return street_types, cities, postcodes


def update_name(name, mapping):

    m = street_type_re.search(name)
    if m:
        street_type = m.group()
        name = name.replace(street_type, mapping[street_type])
        
    return name


def test():
    st_types, cities, postcodes = audit(OSMFILE)
    print repr(postcodes).decode('unicode-escape')

if __name__ == '__main__':
    print sys.stdout.encoding
    reload(sys)
    sys.setdefaultencoding('utf-8')
    
    test()
