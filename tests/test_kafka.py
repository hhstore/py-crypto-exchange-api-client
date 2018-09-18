# -*- coding: utf-8 -*-
from unittest import TestCase
from crypto_exchange.utils.kafka_util import producer, consumer


class TestKafka(TestCase):

    def test_kafka_producer(self):
        future = producer.send('test-python', {'test': 'test'})
        record_metadata = future.get(timeout=10)
        producer.flush()
        print(record_metadata.topic)
        print(record_metadata.partition)
        print(record_metadata.offset)

    def test_kafka_consumer(self):
        while True:
            for msg in consumer:
                print(msg.value)
