import psycopg2


def create_table_gene(cursor):
    sql = """CREATE TABLE GENE(
    ENSEMBL_gene_ID VARCHAR(255) NOT NULL UNIQUE,
    gene_name VARCHAR(255) NOT NULL,
    gene_sequence TEXT NOT NULL UNIQUE,
    gene_description TEXT,

    CONSTRAINT pk_ENSEMBL_gene_ID
    PRIMARY KEY(ENSEMBL_gene_ID)
    )"""
    cursor.execute(sql)
    print("Gene table created!")


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
        create_table_gene(cursor)
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
