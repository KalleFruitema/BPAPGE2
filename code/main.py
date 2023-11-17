"""
File: main.py
Author: Kalle Fruitema
Date: 25/10/2023
Description: De hele database wordt via dit script gemaakt.
Version: Python v3.10.6
"""


import psycopg2

from table_creater import create_all_tables
from table_filler import fill_all_tables


def main():
    """
    Deze functie krijgt geen argumenten mee, en geeft niks terug, 
    er wordt naar de bpapge2 database server connectie gemaakt, 
    dan worden met andere functies alle tables gemaakt en gevuld,
    en hierna worden de veranderingen gecommit en wordt de connectie
    gesloten. Er wordt eerst geprobeerd om alle tabellen te droppen, 
    maar als dit mislukt was de database dus al leeg en gaat het 
    programma verder. Als er een error ergens optreedt na het 
    connecten, wordt de connectie ook gesloten.
    
    :return None:
    """
    print("Program started.")
    conn_string = """
    host='145.97.18.240' dbname='bpapge2_db'
    user='bpapge2' password='bpapge2'
    """
    conn = psycopg2.connect(conn_string)
    print("Connected succesfully.")
    cursor = conn.cursor()
    try:
        try:
            cursor.execute("DROP TABLE alignment, brokstuk, function, "
                           "function_protein, gene, gene_protein, pathway, "
                           "pathway_protein, protein, feature, "
                           "transcript_gene")
            print("Database cleared.")
        except Exception:
            print("Database already empty.")
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
