from pymongo import MongoClient
 

def connect(db = None):

    client = MongoClient()
    db = client.osm
    return db


def count_elem_types(db):
	nodes = db.elements.find({"type": "node"}).count()
	print "Number of nodes:",nodes
	ways =  db.elements.find({"type": "way"}).count()
	print "Number of ways:", ways


def count_users(db):
	users =  db.elements.aggregate([{"$group":{"_id":"$created.user","count":{"$sum":1}}},
									{"$sort":{"count":-1}},
									{"$limit":10}])
	for user in users:
		print user


def elems_on_street(db):
	elems = db.elements.aggregate([{"$match":{"address.street":{"$exists":1}}},
								   {"$group":{"_id": "$address.street", "count":{"$sum":1} }},
								   {"$sort":{"count":-1}},
								   {"$limit":1}])
	for elem in elems:
		print repr(elem).decode('unicode-escape')


def amenity_types(db):
	elems = db.elements.aggregate([{"$match":{"amenity":{"$exists":1}}},
								   {"$group":{"_id": "$amenity", "count":{"$sum":1} }},
								   {"$sort":{"count":-1}},
								   {"$limit":5}])
	for elem in elems:
		print elem


def leisure(db):
	elems = db.elements.aggregate([{"$match":{"leisure":{"$exists":1}}},
								   {"$group":{"_id": "$leisure", "count":{"$sum":1} }},
								   {"$sort":{"count":-1}},
								   {"$limit":5}])
	for elem in elems:
		print elem


if __name__ == '__main__':
 	db = connect()
 	print db.elements.find_one()
 	print db.elements.count()
 	count_elem_types(db)
 	count_users(db)
 	elems_on_street(db)
 	amenity_types(db)
 	leisure(db)

