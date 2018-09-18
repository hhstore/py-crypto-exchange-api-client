# -*- coding: utf-8 -*-
from kafka import KafkaProducer
from kafka import KafkaConsumer
import json


producer = KafkaProducer(bootstrap_servers='192.168.50.190:9092',
                         value_serializer=lambda v: json.dumps(v).encode('utf-8'))

consumer = KafkaConsumer('test-python',
                         group_id='python',
                         bootstrap_servers='192.168.50.190:9092',
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')))


