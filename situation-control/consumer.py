# implements Kafka topic consumer functionality

import threading
from confluent_kafka import Consumer, OFFSET_BEGINNING
import json
from producer import proceed_to_deliver
import base64
from hashlib import sha256
from situation_control import STATE


def handle_event(id, details_str):
    details = json.loads(details_str)
    try:
        delivery_required = False
        if details['operation'] == 'current-position':
                # get the blob for verification from storage
            print(f"Position: {dict.value}")
        elif details['operation'] == 'activate_yourself':  
            STATE = not STATE
    except Exception as e:
        print(f"[error] failed to handle request: {e}")
    if delivery_required:
        proceed_to_deliver(id, details)

def consumer_job(args, config):
    # Create Consumer instance
    verifier_consumer = Consumer(config)

    # Set up a callback to handle the '--reset' flag.
    def reset_offset(verifier_consumer, partitions):
        if args.reset:
            for p in partitions:
                p.offset = OFFSET_BEGINNING
            verifier_consumer.assign(partitions)

    # Subscribe to topic
    topic = "verifier"
    verifier_consumer.subscribe([topic], on_assign=reset_offset)

    # Poll for new messages from Kafka and print them.
    try:
        while True:
            msg = verifier_consumer.poll(1.0)
            if msg is None:
                # Initial message consumption may take up to
                # `session.timeout.ms` for the consumer group to
                # rebalance and start consuming
                # print("Waiting...")
                pass
            elif msg.error():
                print(f"[error] {msg.error()}")
            else:
                # Extract the (optional) key and value, and print.
                try:
                    id = msg.key().decode('utf-8')
                    details_str = msg.value().decode('utf-8')
                    # print("[debug] Consumed event from topic {topic}: key = {key:12} value = {value:12}".format(
                    #     topic=msg.topic(), key=id, value=details_str))
                    handle_event(id, details_str)
                except Exception as e:
                    print(
                        f"[error] Malformed event received from topic {topic}: {msg.value()}. {e}")
    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        verifier_consumer.close()


def start_consumer(args, config):
    threading.Thread(target=lambda: consumer_job(args, config)).start()


if __name__ == '__main__':
    start_consumer(None)
