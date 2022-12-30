import asyncio
from asyncore import loop
from azure.eventhub.aio import EventHubConsumerClient
from azure.eventhub.extensions.checkpointstoreblobaio import BlobCheckpointStore
import os


async def on_event(partition_context, event):
    # Print the event data.
    print("Received the event: \"{}\" from the partition with ID: \"{}\"".format(event.body_as_str(encoding='UTF-8'),
                                                                                 partition_context.partition_id))
    # return event as json then use the entity_id as the delimiter
    # return event.body_as_str(encoding='UTF-8')
    # for each object check entity_id then post object properties to the SQL db

    # Update the checkpoint so that the program doesn't read the events
    # that it has already read when you run it next time.
    await partition_context.update_checkpoint(event)


async def main():
    # Create an Azure blob checkpoint store to store the checkpoints.
    checkpoint_store = BlobCheckpointStore.from_connection_string(os.environ.get('AZURE_STORAGE_CONNECTION_STRING'),
                                                                  os.environ.get('BLOB_CONTAINER_NAME'))

    # Create a consumer client for the event hub.
    client = EventHubConsumerClient.from_connection_string(
        os.environ.get('EVENT_HUBS_NAMESPACE_CONNECTION_STRING'), consumer_group="$Default",
        eventhub_name=os.environ.get('EVENT_HUB_NAME'), checkpoint_store=checkpoint_store)
    async with client:
        # Call the receive method. Read from the beginning of the partition (starting_position: "-1")
        await client.receive(on_event=on_event, starting_position="-1")

    if __name__ == "__main__":
        try:
            asyncio.run(
                main()
            )
        except KeyboardInterrupt:
            pass
    # Run the main method.
    loop.run_until_complete(main())