from kafka import KafkaConsumer
from json import loads
from kafka.structs import TopicPartition

# Kafka broker configuration
# bootstrap_servers = 'localhost:9092'
topic_name = 'postgres.public.student'

# Create Kafka consumer
consumer = KafkaConsumer(
    topic_name,
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset = 'earliest',
    group_id=None,
)


# consumer.assign([TopicPartition(topic_name, 0), TopicPartition(topic_name, 1)])  # Assign partitions 0 and 1


# consumer.poll()
# consumer.seek_to_beginning()
# # print('partitions of the topic: ',consumer.partitions_for_topic(topic_name))

print(f"Subscribed to topic: {topic_name}")
# Start consuming messages
for message in consumer:
    print('easter egg')
    print(f"Received message: {message.value}")
    # Process the message here...