import pymongo
from pymongo.errors import DuplicateKeyError

def mongo():
    # client = pymongo.MongoClient('10.9.60.13', 27017, username='olbase', password='mongodb', authSource='OLBASE', authMechanism='DEFAULT')
    client = pymongo.MongoClient('localhost', 27017)
    db = client.OLBASE
    collection = db.en_olbase
    # collection.remove({'WGK Germany:': '3'})
    return collection

def repeat():
    # client = pymongo.MongoClient('10.9.60.13', 27017, username='olbase', password='mongodb', authSource='OLBASE', authMechanism='DEFAULT')
    client = pymongo.MongoClient('localhost', 27017)
    db = client.molbase
    collection = db.en_olbase_repeat
    # collection.remove({'WGK Germany:': '3'})
    return collection

def en_cache():
    # client = pymongo.MongoClient('10.9.60.13', 27017, username='olbase', password='mongodb', authSource='OLBASE', authMechanism='DEFAULT')
    client = pymongo.MongoClient('localhost', 27017)
    db = client.OLBASE
    collection = db.en_cache
    # collection.remove({'WGK Germany:': '3'})
    return collection

def en_olbase_url():
    # client = pymongo.MongoClient('10.9.60.13', 27017, username='olbase', password='mongodb', authSource='OLBASE', authMechanism='DEFAULT')
    client = pymongo.MongoClient('localhost', 27017)
    db = client.OLBASE
    collection = db.en_olbase_url
    # collection.remove({'WGK Germany:': '3'})
    return collection

def en_olbase_err():
    # client = pymongo.MongoClient('10.9.60.13', 27017, username='olbase', password='mongodb', authSource='OLBASE', authMechanism='DEFAULT')
    client = pymongo.MongoClient('localhost', 27017)
    db = client.OLBASE
    collection = db.en_olbase_err_url
    # collection.remove({'WGK Germany:': '3'})
    return collection

db_en_olbase = mongo()
db_en_olbase_url = en_olbase_url()
db_en_cache = en_cache()
db_en_err = en_olbase_err()


if __name__ == '__main__':
    mongo()