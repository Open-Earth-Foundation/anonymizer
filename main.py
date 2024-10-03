from utils.message_retriever import retrieve_messages_list
from anonymizer.utils.json_exporter import export_to_json
from utils.extract_messages_infos import extract_messages_info
from utils.anonymizer import anonymize_messages_object
from anonymizer.utils.thread_ids_importer import import_thread_ids
from anonymizer.utils.db_exporter import export_to_db

# Example usage
if __name__ == "__main__":

    # Create a list of thread ids to extract messages and to anonymize
    thread_ids = []

    # Load the thread ids from a stored db
    thread_ids = import_thread_ids()

    # List of raw threads
    raw_threads = []

    # List of anonymized threads
    anonymized_threads = []

    for thread_id in thread_ids:
        print(f"Thread ID: {thread_id}")

        # Get the raw messages object from openAI
        messages_list_raw = retrieve_messages_list(thread_id)

        if messages_list_raw:
            # Prefilter the relevant information from the thread messages object
            messages_dict = extract_messages_info(messages_list_raw)

            # Write the raw messages object to a file -> needs to be removed later as we do not want to store this info
            raw_threads.append(messages_dict)

            # Anonymize the messages object and write anonymized output to a file for storage
            # Method either 'huugingface' or 'spacy'
            messages_dict_anonymized = anonymize_messages_object(
                messages_dict, method="huggingface"
            )
            anonymized_threads.append(messages_dict_anonymized)
        else:
            print("No messages found or an error occurred.")

    export_to_json(raw_threads, "raw.json")
    export_to_json(anonymized_threads, "anonymized.json")

    # Write the anonymized data to the database
    export_to_db(anonymized_threads)
