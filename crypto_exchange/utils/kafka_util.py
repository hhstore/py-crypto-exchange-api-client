# -*- coding: utf-8 -*-
from kafka import KafkaProducer
from kafka import KafkaConsumer
import json


class JsonKafkaClient:

    @staticmethod
    def producer(host: str=None):
        producer = KafkaProducer(bootstrap_servers=host or '192.168.50.190:9092',
                                 value_serializer=lambda v: json.dumps(v).encode('utf-8'))
        return producer

    @staticmethod
    def consumer(topics, host: str=None, group_id=None):
        if isinstance(topics, list) or isinstance(topics, str):
            consumer = KafkaConsumer(topics,
                                     group_id=group_id or 'default',
                                     bootstrap_servers=host or '192.168.50.190:9092',
                                     value_deserializer=lambda m: json.loads(m.decode('utf-8')))
            return consumer
        else:
            return KafkaConsumer('default',
                                 group_id=group_id or 'default',
                                 bootstrap_servers=host or '192.168.50.190:9092',
                                 value_deserializer=lambda m: json.loads(m.decode('utf-8')))
