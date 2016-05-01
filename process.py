#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json
"""


{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}


"""


lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
street_type_re = re.compile(ur'\b[а-я][а-яА-ЯЁё-]+\.?', re.U,)
postcode_re = re.compile(ur'^1[89][0-9]{4}', re.U)

CREATED = ["version", "changeset", "timestamp", "user", "uid"]
city_name = u"Санкт-Петербург"

mapping = { u"пр.": u"проспект",
            u"пр": u"проспект",
            u"пл.": u"площадь",
            u"ул.": u"улица"
            }


problem = [u"ул." , u"пр.", u"пер.", u"бул.", u"наб.", u"пл."]             

def is_city_name(elem):
    return (elem == "addr:city")


def is_street_name(elem):
    return (elem == "addr:street")



def is_postcode(elem):
    return (elem == "postal_code" or elem == "addr:postcode")


def process_attribs(node, element):

    for attr, value in element.attrib.items():
        
        if attr in CREATED:
            if "created" not in node.keys():
                node['created'] = {}
            node['created'][attr] = value
        elif attr == 'lat' or attr == 'lon':
            if 'pos' not in node.keys():
                node['pos'] = [0.0,0.0]
            if attr == 'lat':
                node['pos'][0] = float(value)
            else:
                node['pos'][1] = float(value)
                
        else:
            node[attr] = value


def process_city(value):
    if value == "St. Petersburg":
        print value
        return city_name
    else:
        return value


def process_street(name):

    m = street_type_re.search(unicode(name))
    if m:
        street_type = m.group()
        if street_type in problem:
            print street_type
            name = name.replace(street_type, mapping[unicode(street_type)])
        
    return name


def not_valid_postcode(value):

    m = postcode_re.match(unicode(value))
    if m:
        return False
    else:
        return True

def fill_address(node, key, value):

    key = key.replace('addr:',"")
    if ":" in key:
        return
    if 'address' not in node.keys():
        node['address'] = {}
    node['address'][key] = value
 

def process_child(node, child, element):

    if child.tag == 'tag':
 
        key = child.attrib['k']
        value = child.attrib['v']

        if problemchars.search(key):
            return
        if is_city_name(key):
            value = process_city(value)
        if is_street_name(key):
            value = process_street(value)
        if is_postcode(key):
            if not_valid_postcode(value):
                return
        if key.startswith('addr:'):
            fill_address(node, key, value)
        else:
            node[key] = value

    elif child.tag == 'nd' and element.tag == 'way':
        if 'node_refs' not in node.keys():
            node['node_refs'] = []
        node['node_refs'].append(child.attrib['ref'])
        #print key


def shape_element(element):

    node = {}
    if element.tag == "node" or element.tag == "way" :
        node['type'] = element.tag 
        
        #processing attributes
        process_attribs(node, element)
 
                
        #processing second level tags
        for child in element:
            process_child(node, child, element)
            
        #print node
        return node
    else:
        return None


def process_map(file_in, pretty = False):
    
    tags=('node', 'way', 'relation')
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w", encoding = 'utf-8') as fo:
        for event, elem in ET.iterparse(file_in):
            el = shape_element(elem)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el, ensure_ascii = False) + "\n")
            #if event == 'end' and elem.tag in tags:
                #elem.clear()
    return data

def test():
    #data = process_map('piter_small.osm', pretty=False)
    data = process_map('saint-petersburg.osm', pretty=False)
    #pprint.pprint(data)
    
  

if __name__ == "__main__":
    test()