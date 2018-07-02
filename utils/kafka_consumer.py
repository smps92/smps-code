from pykafka import KafkaClient
import json
import os
import sys


class PyKafkaConsumer:
    def __init__(self, config_dict):
        self.config_dict = config_dict
        self.bootstrap_servers = self.config_dict["bootstrap_servers"] # kafka bootstrap server
        self.topic = bytes(self.config_dict['topics'])

    def consume_from_kafka(self):
        kafka_client = KafkaClient(hosts=self.bootstrap_servers)
        topic = kafka_client.topics[self.topic]
        consumer = topic.get_simple_consumer()
        for msg in consumer:
            if msg is not None:
                print(json.loads(msg.value))


if __name__ == "__main__":
    with open(sys.argv[1], "r") as fd:
        config_dict = json.load(fd)
    py_kafka_consumer = PyKafkaConsumer(config_dict['kafka']['output'])
    py_kafka_consumer.consume_from_kafka()
