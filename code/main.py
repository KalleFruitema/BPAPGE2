import psycopg2
from table_creater import *
from table_filler import *


def create_all_tables(cursor):
    print("me in function")
    create_table_brokstuk(cursor)
    create_table_gene(cursor)
    create_table_alignment(cursor)
    create_table_function(cursor)
    create_table_pathway(cursor)
    create_table_protein(cursor)
    create_table_pathway_protein(cursor)
    create_table_function_protein(cursor)
    create_table_gene_protein(cursor)
    create_table_spliced_gene(cursor)
    print("All tables created!")


def fill_all_tables(cursor):
    align_data, gene_data, protein_data, \
    pathway_data, function_data, function_data_ids = get_table_data()
    fill_table_brokstuk(cursor)
    fill_table_gene(cursor, gene_data)
    fill_table_alignment(cursor, align_data)
    fill_table_protein(cursor, protein_data)
    fill_table_gene_protein(cursor, protein_data)
    fill_table_pathway(cursor, pathway_data)
    fill_table_pathway_protein(cursor, pathway_data)
    fill_table_function(cursor, function_data_ids)
    fill_table_function_protein(cursor, function_data, function_data_ids)
    print("All tables filled!")


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
