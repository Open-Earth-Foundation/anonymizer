def extract_message_content(messages):
    print(f"Retrieved {len(messages)} messages:\n")
    for i, message in enumerate(messages, start=1):
        for content_block in message.content:
            if hasattr(content_block, "text") and hasattr(content_block.text, "value"):
                # Extract and print the 'value' from the 'text' object
                print(f"Message {i}: {content_block.text.value}")
