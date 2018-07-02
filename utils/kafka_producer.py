
import json
import time
from pykafka import KafkaClient


class PyKafkaProducer:
    def __init__(self, config_dict):
        self.config_dict = config_dict
        self.bootstrap_servers = bytes(self.config_dict["bootstrap_servers"]) # kafka bootstrap server
        self.topic = bytes(self.config_dict['topics']) 
        self.producer_sync = bool(self.config_dict['sync_producer']) # block till kafka flushes the messages
        self.producer_auto_start = bool(self.config_dict['auto_start']) # start the producer immediately
        self.linger_ms = int(self.config_dict['linger_ms']) # In Spark terms, this is the batch interval for Kafka,
                                                       # Kafka waits for linger_ms before flushing the queue

    def send_to_kafka(self, processedTxns):
        kclient = KafkaClient(hosts=self.bootstrap_servers)
        topic = kclient.topics[self.topic]
        producer = topic.get_producer(sync=self.producer_sync,
                                      auto_start=self.producer_auto_start,
                                      linger_ms=self.linger_ms)
        for txn in processedTxns:
            #print("start time to produce={}".format(time.time()))
            producer.produce(json.dumps(txn))
            #print("end time to produce={}\n\n\n".format(time.time()))	
        producer.stop()
