import psycopg
from utils.db_connector import connect_to_db
from datetime import datetime


def export_messages(anonymized_threads):
    """
    This function exports the anonymized messages to the database.
    It updated only new messages with new assistant_message_id.
    """

    try:
        conn = connect_to_db()
        cur = conn.cursor()
        current_timestamp = datetime.now()

        for item in anonymized_threads:
            # Extract meta_data
            meta_data = item.get("meta_data", {})
            thread_id = meta_data.get("ThreadID")

            if not thread_id:
                print("Missing ThreadID in meta_data. Skipping this item.")
                continue

            # Process messages
            messages = item.get("messages", [])
            for message in messages:
                assistant_message_id = message.get("id")
                role = message.get("role")
                created_at_unix = message.get("created_at")
                content = message.get("content")

                if not all([assistant_message_id, role, created_at_unix, content]):
                    print(
                        f"Missing fields in message {message}. Skipping this message."
                    )
                    continue

                # Convert UNIX timestamp to datetime
                message_timestamp = datetime.fromtimestamp(created_at_unix)

                # Insert into AssistantMessage
                insert_message_query = """
                INSERT INTO public."AssistantMessage" (
                    assistant_message_id,
                    thread_id,
                    role,
                    timestamp,
                    content,
                    created,
                    last_updated
                ) VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (assistant_message_id) DO NOTHING;
                """
                cur.execute(
                    insert_message_query,
                    (
                        assistant_message_id,
                        thread_id,
                        role,
                        message_timestamp,
                        content,
                        current_timestamp,
                        current_timestamp,
                    ),
                )

        # Commit the transaction
        conn.commit()
        print("Data inserted successfully.")

    except psycopg.Error as e:
        print(f"Database error: {e}")

    finally:
        # Close the cursor and connection
        if cur:
            cur.close()
        if conn:
            conn.close()
