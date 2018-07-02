
from utils.kafka_consumer import PyKafkaConsumer
import json
import os


def test_kafka_consumer():
    with open(os.getcwd()+"/config/main_config_aws.json", "r") as fd:
        config_dict = json.load(fd)
    py_kafka_consumer = PyKafkaConsumer(config_dict['kafka']['output'])
    py_kafka_consumer.consume_from_kafka()


if __name__ == "__main__":
    test_kafka_consumer()