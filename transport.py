import time
from azure.eventhub import EventHubConsumerClient, Receiver, Offset
import json

with open('local.settings.json','r') as f:
    data = json.load(f)

json_str = json.dumps(data)

auth = json.loads(json_str)

# Connect to the Event Hub
event_hub_client = EventHubConsumerClient.from_connection_string(
    conn_str=auth['EVENT_HUBS_NAMESPACE_CONNECTION_STRING'],
    eventhub_name=auth['EVENT_HUB_NAME']
)

# Create a receiver to read messages from the Event Hub
Receiver = event_hub_client.create_consumer(
    consumer_group='$Default',
    partition_id='1',
    event_position=Offset(-1),
    prefetch=100
)

# Connect to the MySQL database
import mysql.connector

mydb = mysql.connector.connect(
  host=auth['DBHOST'],
  user=auth['DBUSER'],
  password=auth['DBPASS'],
  database=auth['DB']
)

# Continuously read messages from the Event Hub and update the MySQL database
while True:
    # Get a batch of messages from the Event Hub
    messages = Receiver.receive(timeout=10)

    # Insert the messages into the MySQL database
    cursor = mydb.cursor()
    for message in messages:
        sql = 'INSERT INTO device (device_id, device_brand, device_model, device_name, is_smart_device, has_battery, is_on) VALUES ("entity_id", "iPhone", "8", "iPhone_8_no_1", 1,0)'
        val = (message.field1, message.field2, message.field3, message.field4, message.field5, message.field6, message.field7)
        cursor.execute(sql, val)
        mydb.commit()
    cursor.close()

    # Sleep for 10 minutes
    time.sleep(600)