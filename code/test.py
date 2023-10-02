import psycopg2


def create_table_brokstuk(cursor):
    print("in brokstuk func")
    sql = """CREATE TABLE BROKSTUK(
    brokstuk_header VARCHAR(255) NOT NULL UNIQUE,
    brokstuk_sequence TEXT NOT NULL UNIQUE,

    CONSTRAINT pk_brokstuk_header
    PRIMARY KEY(brokstuk_header)
    )"""
    print("Ik ga nu naar execute toe:")
    cursor.execute(sql)
    print("Brokstuk table created!")


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
        create_table_brokstuk(cursor)
        # create_all_tables(cursor)
        print("Filling tables...")
        # fill_all_tables(cursor)
        
        conn.commit()
        conn.close()
        print('Succes! Closing connection.')
    except Exception as e:
        conn.close()
        print("Error: ", e)

if __name__ == "__main__":
    main()
