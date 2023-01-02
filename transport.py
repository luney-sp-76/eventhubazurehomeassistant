import time
from azure.eventhub import EventHubClient, Receiver, Offset

# Connect to the Event Hub
event_hub_client = EventHubClient.from_connection_string(
    conn_str='<event_hub_connection_string>',
    eventhub_name='<event_hub_name>'
)

# Create a receiver to read messages from the Event Hub
receiver = event_hub_client.create_consumer(
    consumer_group='<consumer_group_name>',
    partition_id='<partition_id>',
    event_position=Offset('<offset>'),
    prefetch=100
)

# Connect to the MySQL database
import mysql.connector

mydb = mysql.connector.connect(
  host='<database_host>',
  user='<database_username>',
  password='<database_password>',
  database='<database_name>'
)

# Continuously read messages from the Event Hub and update the MySQL database
while True:
    # Get a batch of messages from the Event Hub
    messages = receiver.receive(timeout=10)

    # Insert the messages into the MySQL database
    cursor = mydb.cursor()
    for message in messages:
        sql = 'INSERT INTO <table_name> (field1, field2, field3) VALUES (%s, %s, %s)'
        val = (message.field1, message.field2, message.field3)
        cursor.execute(sql, val)
        mydb.commit()
    cursor.close()

    # Sleep for 10 minutes
    time.sleep(600)