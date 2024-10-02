from utils.message_retriever import retrieve_messages_list
from utils.write_to_json import write_output_to_file
from utils.extract_messages_infos import extract_messages_info


# Example usage
if __name__ == "__main__":

    thread_id = "thread_FyKAKtGCH7vMSFdv69pgmk76"
    messages = retrieve_messages_list(thread_id)

    if messages:
        messages_info = extract_messages_info(messages)

        write_output_to_file(messages_info, "output.json")

    else:
        print("No messages found or an error occurred.")
