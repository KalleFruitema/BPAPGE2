import psycopg2


def query(cursor):
    sql = """SELECT ncbi_prot_id, prot_sequence FROM protein"""
    cursor.execute(sql)

    row = cursor.fetchone()
    fasta_str = ''

    while row is not None:
        fasta_str += f">{row[0]}\n{row[1]}\n"
        row = cursor.fetchone()
    with open("results/panthera_pardus_proteins", "w+") as fasta_file:
        fasta_file.write(fasta_str)


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
        
        query(cursor)

        # conn.commit()
        conn.close()
        print('Succes! Closing connection.')
    except Exception as e:
        conn.close()
        print("Error: ", e)

if __name__ == "__main__":
    main()
