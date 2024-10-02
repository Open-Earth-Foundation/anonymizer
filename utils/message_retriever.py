from utils.create_client import create_client

client = create_client()


def retrieve_messages_list(thread_id):
    try:
        # Call OpenAI's Assistant API to list messages by thread ID
        response = client.beta.threads.messages.list(
            thread_id=thread_id,
        )
        # Extract and return the messages
        return response.data

    except Exception as e:
        print(f"Error retrieving messages: {str(e)}")
        return None
