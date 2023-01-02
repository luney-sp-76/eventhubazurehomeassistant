import asyncio
from azure.eventhub.aio import EventHubConsumerClient as client
from azure.eventhub.extensions.checkpointstoreblobaio import BlobCheckpointStore
import json

with open('local.settings.json','r') as f:
    data = json.load(f)

json_str = json.dumps(data)

auth = json.loads(json_str)


async def on_event(partition_context, event):
    # Print the event data.
    print("Received the event: \"{}\" from the partition with ID: \"{}\"".format(event.body_as_str(encoding='UTF-8'), partition_context.partition_id))

    # Update the checkpoint so that the program doesn't read the events
    # that it has already read when you run it next time.
    await partition_context.update_checkpoint(event)

async def main():
    # Create an Azure blob checkpoint store to store the checkpoints.
    checkpoint_store = BlobCheckpointStore.from_connection_string(auth['AZURE_STORAGE_CONNECTION_STRING'], "homeassistant")

    # Create a consumer client for the event hub.
    async with client:
        # Call the receive method. Read from the beginning of the partition (starting_position: "-1")
        await client.receive(on_event=on_event,  starting_position="-1")


if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        asyncio.run(main(loop=loop))
    except KeyboardInterrupt:
        pass