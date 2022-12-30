import asyncio
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
import os

async def run(x):
    # Create a producer client to send messages to the event hub.
    # Specify a connection string to your event hubs namespace and
    # the event hub name.
    producer = EventHubProducerClient.from_connection_string(conn_str=os.environ.get('CONNECTION_STRING'), eventhub_name=os.environ.get('EVENT_HUB_NAME'))
    async with producer:
        # Create a batch.
        event_data_batch = await producer.create_batch()

        # Add events to the batch.
        event_data_batch.add(EventData(x))

        # Send the batch of events to the event hub.
        await producer.send_batch(event_data_batch)

# loop = asyncio.get_event_loop()

if __name__ == "__run__":
    try:
        asyncio.run(
            run('on')
        )
    except KeyboardInterrupt:
        pass
    # Run the main method.
    #loop.run_until_complete(main())  
   
#loop.run_until_complete(run())