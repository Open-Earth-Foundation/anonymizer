import psycopg
from utils.db_connector import connect_to_db
from datetime import datetime


def export_messages(anonymized_threads):

    try:
        conn = connect_to_db()
        cur = conn.cursor()

        for item in anonymized_threads:
            # Extract meta_data
            meta_data = item.get("meta_data", {})
            thread_id = meta_data.get("ThreadID")
            assistant_id = meta_data.get("assistant_id")

            if not thread_id or not assistant_id:
                print(
                    "Missing ThreadID or assistant_id in meta_data. Skipping this item."
                )
                continue

            # Update AssistantThread with assistant_id
            upsert_thread_query = """
            INSERT INTO public."AssistantThread" (
                assistant_thread_id,
                assistant_id
            ) VALUES (%s, %s)
            ON CONFLICT (assistant_thread_id) DO UPDATE SET
                assistant_id = EXCLUDED.assistant_id
            WHERE public."AssistantThread".assistant_id IS DISTINCT FROM EXCLUDED.assistant_id;
            """
            cur.execute(upsert_thread_query, (thread_id, assistant_id))

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
                created_at = datetime.fromtimestamp(created_at_unix)

                # Insert into AssistantMessages
                insert_message_query = """
                INSERT INTO public."AssistantMessages" (
                    assistant_message_id,
                    thread_id,
                    role,
                    created_at,
                    content
                ) VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (assistant_message_id) DO NOTHING;
                """
                cur.execute(
                    insert_message_query,
                    (
                        assistant_message_id,
                        thread_id,  # The ThreadID from meta_data
                        role,
                        created_at,
                        content,
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
