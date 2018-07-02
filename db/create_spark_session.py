

import json
from pyspark import SparkContext,SparkConf
from pyspark.sql import SparkSession
from pyspark.streaming.kafka08 import KafkaUtils
from pyspark.sql.types import StringType
from pyspark.streaming import StreamingContext


class MongoKafkaSession:

    def __init__(self, config_dict):
        self.json_dict = config_dict
        self.kafka_config = self.json_dict['kafka']
        self.mongo_config = self.json_dict['mongo']
        self.spark_config = self.json_dict['spark']

    def get_mongo_conn_string(self, json_conf):
        mongo_conn_string = "mongodb://{}:{}@{}:{}/{}.{}".format(json_conf['username'],
                                                                json_conf['password'],
                                                                json_conf['host'],
                                                                json_conf['port'],
                                                                json_conf['db'],
                                                                json_conf['collection'])
        return mongo_conn_string

    def get_mongo_kafka_session(self):
        mongo_conn_string = self.get_mongo_conn_string(self.mongo_config['v'])
        spark_session = SparkSession.builder\
            .appName("v") \
            .config('spark.mongodb.input.uri', mongo_conn_string)  \
            .config('spark.mongodb.output.uri', mongo_conn_string) \
            .getOrCreate()
        spark_context = spark_session.sparkContext
        streaming_context = StreamingContext(spark_context, self.spark_config['batchInterval'])
        spark_context.setLogLevel("ERROR")
        return spark_session, streaming_context


class KafkaSession:

    def __init__(self, config_dict):
        self.json_dict = config_dict
        self.kafka_config = self.json_dict['kafka']
        self.mongo_config = self.json_dict['mongo']
        self.spark_config = self.json_dict['spark']

    def get_kafka_session(self):
        spark_session = SparkSession.builder \
            .appName("v") \
            .getOrCreate()
        spark_context = spark_session.sparkContext
        streaming_context = StreamingContext(spark_context, self.spark_config['batchInterval'])
        spark_context.setLogLevel("ERROR")
        return spark_session, streaming_context


#class mongoMongoSession:

#class kafkaMongoSession:

