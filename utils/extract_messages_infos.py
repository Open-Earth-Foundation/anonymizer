def extract_messages_info(messages):
    """
    Extracts relevant information from a list of messages and structures it into
    a dictionary with 'meta_data' and 'messages' keys. The messages are sorted
    from oldest to latest based on the 'created_at' timestamp.

    Additionally, it searches for the first non-null assistant_id to include in meta_data.

    Args:
        messages (list): A list of message objects retrieved from the API.

    Returns:
        dict: A dictionary containing 'meta_data' and 'messages' as per the desired schema.
    """
    if not messages:
        return {"meta_data": {"ThreadID": None, "assistant_id": None}, "messages": []}

    sorted_messages = sorted(messages, key=lambda msg: msg.created_at)

    thread_id = sorted_messages[0].thread_id

    # Initialize assistant_id as None
    assistant_id = None

    # Iterate through messages to find the first non-null assistant_id
    for msg in sorted_messages:
        if msg.assistant_id:
            assistant_id = msg.assistant_id
            break

    messages_list = []
    for message in sorted_messages:
        # Extract content from content blocks
        content_values = []
        for content_block in message.content:
            # Check if the content block has 'text' and 'value' attributes
            if hasattr(content_block, "text") and hasattr(content_block.text, "value"):
                content_values.append(content_block.text.value)

        # Combine all content values into a single string
        content = " ".join(content_values)

        # Structure the message information
        message_info = {
            "id": message.id,
            "role": message.role,
            "created_at": message.created_at,
            "content": content,
        }
        messages_list.append(message_info)

    return {
        "meta_data": {"ThreadID": thread_id, "assistant_id": assistant_id},
        "messages": messages_list,
    }
