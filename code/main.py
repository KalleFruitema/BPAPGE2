import psycopg2
from table_creater import create_all_tables
from table_filler import fill_all_tables


def main():
    print("Program started.")
    conn_string = """
    host='145.97.18.240' dbname='bpapge2_db'
    user='bpapge2' password='bpapge2'
    """
    conn = psycopg2.connect(conn_string)
    print("Connected succesfully.")
    cursor = conn.cursor()
    try:
        print("Creating tables...")
        create_all_tables(cursor)
        print("Filling tables...")
        fill_all_tables(cursor)
        
        conn.commit()
        conn.close()
        print('Succes! Closing connection.')
    except Exception as e:
        conn.close()
        print("Error: ", e)

if __name__ == "__main__":
    main()
