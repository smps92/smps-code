from pymongo import MongoClient
from pymongo.errors import PyMongoError
import logging
import ssl
import os
import datetime
import json


def get_mongo_conn(host, port, username, password, db, ssl=False):

    if ssl:
#        client = MongoClient(host, port, ssl=True, replicaSet='rs0', w=2, ssl_cert_reqs=ssl.CERT_NONE)
        client = MongoClient(host, port, ssl=True, ssl_cert_reqs=ssl.CERT_NONE)
    else:
        client = MongoClient(host, port)
#        client = MongoClient(host, port, replicaSet='rs0', w=2)
    try:
        mongodb = client[db]
        mongodb.authenticate(
            name=username,
            password=password,
        )
    except PyMongoError:
        raise  # TODO: Adding logging and capture this error
    return mongodb



class BaseMongo(object):

    def __init__(self, config=None):
        self.config = config
        self.db_read_conn = get_mongo_conn(self.config['readHost'],
                                         self.config['readPort'],
                                         self.config['username'],
                                         self.config['password'],
                                         self.config['source'])

        self.db_write_conn = get_mongo_conn(self.config['host'],
                                          self.config['port'],
                                          self.config['username'],
                                          self.config['password'],
                                          self.config['source'])

    def mongo_find(self, filter_query, project=None, collection='transactions'):
        return self.db_read_conn[collection].find(filter=filter_query, projection=project)

    def mongo_find_one(self, filter_query, project=None, collection='transactions'):
        return self.db_read_conn[collection].find_one(filter=filter_query, projection=project)

    def mongo_aggregate(self, pipeline, collection='transactions'):
        return self.db_read_conn[collection].aggregate(pipeline)

    def mongo_count(self, query, collection='transactions'):
        return self.db_read_conn[collection].count(query)

    def mongo_update_one(self, filter_query, updates, collection='transactions'):
        return self.db_write_conn[collection].update_one(filter_query,updates)

    def mongo_update(self, filter_query, updates, collection='transactions'):
        return self.db_write_conn[collection].update(filter_query, updates)

    def mongo_update_many(self, filter_query, updates, collection='transactions'):
        return self.db_write_conn[collection].update_many(filter_query, updates)

    def mongo_remove(self, del_query, collection='transactions'):
        return self.db_write_conn[collection].remove(del_query)

    def mongo_insert(self, transaction, collection='transactions'):
        return self.db_write_conn[collection].insert_one(transaction)


class VMongo(BaseMongo):

    def __init__(self, mongo_conf_dict, logger=None):
        self.v_mongo_conf = mongo_conf_dict['vt']
        super(VMongo, self).__init__(self.v_mongo_conf)


class WMongo(BaseMongo):

    def __init__(self, mongo_conf_dict, logger=None):
        self.w_mongo_conf = mongo_conf_dict['W']
        super(WMongo, self).__init__(self.w_mongo_conf)


def create_mongo_db_conn(mongo_conf):

    v_mongo_obj = VMongo(mongo_conf['mongo'])
    w_mongo_obj = WMongo(mongo_conf['mongo'])
    return v_mongo_obj, w_mongo_obj
