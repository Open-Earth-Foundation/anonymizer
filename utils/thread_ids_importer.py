import psycopg
from utils.db_connector import connect_to_db


def import_thread_ids():
    # Connect to Db
    try:
        # Call the function to get the connection object
        conn = connect_to_db()
        with conn.cursor() as cur:
            query = 'SELECT assistant_thread_id FROM public."AssistantThread";'
            cur.execute(query)
            thread_ids = [row[0] for row in cur.fetchall()]
        conn.close()
        print(f"Thread IDs: {thread_ids}")
        return thread_ids
    except psycopg.Error as e:
        print(f"Database error: {e}")
        return []

    # Hard coded for now
    thread_ids = [
        "thread_8QV0nMoGUprwNIjB1x1IkIqz",
        "thread_FyKAKtGCH7vMSFdv69pgmk76",
        "thread_Li0DPzpJaANEwKc2JXNd9XOH",
        "thread_0j74ndYUJRQp1rQtbVhLVDHB",
    ]
    return thread_ids
