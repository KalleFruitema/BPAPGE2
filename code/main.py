import psycopg2
from table_creater import *
from table_filler import *


def create_all_tables(cursor):
    create_table_brokstuk(cursor)
    create_table_gene(cursor)
    create_table_alignment(cursor)
    create_table_function(cursor)
    create_table_pathway(cursor)
    create_table_protein(cursor)
    create_table_pathway_protein(cursor)
    create_table_fuction_protein(cursor)
    create_table_gene_protein(cursor)
    create_table_spliced_gene(cursor)


def fill_all_tables(cursor):
    # hoe dit werkt is tijdelijk, ik maak later een functie in table_filler.py om alles te vullen
    # (daarnaast geeft het waarschijnlijk nu een error dus voor testen run gwn table_filler.py ipv main.py)
    tf_main(cursor)


def main():    
    conn_string = """
    host='145.97.18.240' dbname='bpapge2_db'
    user='bpapge2' password='bpapge2'
    """
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    try:       
        create_all_tables(cursor)

        fill_all_tables(cursor)
        
        conn.commit()
        conn.close()
        print('Succes!')
    except Exception as e:
        conn.close()
        print("Error: ", e)

if __name__ == "__main__":
    main()
