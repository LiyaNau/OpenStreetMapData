from pymongo import MongoClient
import json
import codecs

def insert_data(data, db):

    db.elements.insert(data)


if __name__ == "__main__":
	client = MongoClient()
	db = client.osm

	with codecs.open('saint-petersburg.osm.json','rb',encoding = 'utf-8') as f:

		for line in f:
	    		data = json.loads(unicode(line))
	    		insert_data(data, db)

	print db.elements.find_one()

