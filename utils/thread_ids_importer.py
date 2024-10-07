import psycopg
from utils.db_connector import connect_to_db


def import_thread_ids():
    """
    This function imports the thread ids from the database.
    It only imports the thread ids from 'AssistantThread' that are not yet in 'AssistantMessage' and therfore have not been processed yet.
    """

    try:
        conn = connect_to_db()
        with conn.cursor() as cur:
            query = """
            SELECT assistant_thread_id
            FROM public."AssistantThread"
            WHERE assistant_thread_id NOT IN (
                SELECT DISTINCT thread_id FROM public."AssistantMessage"
            );
            """
            cur.execute(query)
            thread_ids = [row[0] for row in cur.fetchall()]
        conn.close()
        print(f"Thread IDs: {thread_ids}")
        return thread_ids
    except psycopg.Error as e:
        print(f"Database error: {e}")
        return []
