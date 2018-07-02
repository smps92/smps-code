import os
import json
from utils.kafka_producer import PyKafkaProducer


def test_kafka_producer():
    with open(os.getcwd()+"/config/main_cfg_aws.json", "r") as fd:
        config_dict = json.load(fd)
    with open(os.getcwd()+"/tests/sampleTransaction", "r") as fd:
        json_txn = json.load(fd)
    kproducer = PyKafkaProducer(config_dict['kafka']['output'])
    kproducer.send_to_kafka([json_txn])


if __name__ == "__main__":
    test_kafka_producer()
