"""
File: table_filler.py
Author: Kalle Fruitema
Date: 25/10/2023
Description: Haalt alle data op en vult alle tabellen hiermee.
Version: Python v3.10.6
"""


import json
import os

from Bio import SeqIO
import requests


def fill_table_brokstuk(cursor):
    """
    Deze functie leest 'seq2.fa' in om de sequenties te krijgen
    zodat de brokstuk tabel gevuld kan worden. De inhoud van 
    het bestand wordt geparsed en de inhoud wordt in de 
    database gezet.

    :param cursor: Dit object wordt gebruikt om de sql code te 
    runnen op de database server.
    :return None:
    """
    with open('data/seq2.fa') as file:
        inhoud = file.read().strip().split('\n')
    fasta_dict = {}
    for i, line in enumerate(inhoud):
        if line[0] == '>': 
            fasta_dict.update({
                line: inhoud[i+1]
            })
    for key_val in fasta_dict.items():
        sql = """INSERT INTO BROKSTUK
        VALUES(%s, %s)"""
        cursor.execute(sql, key_val)
    print("Brokstuk table filled.")


def fill_table_alignment(cursor, data):
    """
    Deze functie krijgt data, en vult de alignment tabel
    met deze data.

    :param cursor: Dit object wordt gebruikt om de sql code te 
    runnen op de database server.
    :param data: lijst met lijsten erin, met de data die in de
    database wordt gezet.
    :return None:
    """
    sql = """INSERT INTO ALIGNMENT
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
    for line in data:
        cursor.execute(sql, line)
    print("Alignment table filled.")


def fill_table_transcript_gene(cursor, data):
    """
    Deze functie krijgt data, en vult de transcript_gene tabel
    met deze data.

    :param cursor: Dit object wordt gebruikt om de sql code te 
    runnen op de database server.
    :param data: lijst met lijsten erin, met de data die in de
    database wordt gezet.
    :return None:
    """
    sql = """INSERT INTO TRANSCRIPT_GENE
    VALUES(%s, %s)"""
    for line in data:
        cursor.execute(sql, line)
    print("Transcript_gene table filled.")


def fill_table_gene(cursor, data):
    """
    Deze functie krijgt data, en vult de gene tabel
    met deze data.

    :param cursor: Dit object wordt gebruikt om de sql code te 
    runnen op de database server.
    :param data: lijst met lijsten erin, met de data die in de
    database wordt gezet.
    :return None:
    """
    sql = """INSERT INTO GENE
    VALUES(%s, %s, %s, %s)"""
    for line in data:
        cursor.execute(sql, line)
    print("Gene table filled.")


def fill_table_protein(cursor, data):
    """
    Deze functie krijgt een lijst met dictionaries van data, checkt 
    door middel van een set met tuples er in of er dubbele waarden 
    zijn, en zorgt er ook gelijk voor dat de juiste waarden worden 
    gebruikt uit de dicts. Daarna wordt de protein tabel van de 
    database met deze set gevuld.

    :param cursor: Dit object wordt gebruikt om de sql code te 
    runnen op de database server.
    :param data: lijst met dictionaries er in, met de data die in de
    database wordt gezet.
    :return None:
    """
    sql = """INSERT INTO PROTEIN
    VALUES(%s, %s, %s)"""
    data_check = set()
    for item in data:
        data_check.add(tuple([item["NCBI_prot_ID"], item["prot_name"], 
                              item["prot_sequence"]]))
    for line in data_check:
        cursor.execute(sql, line)
    print("Protein table filled.")


def fill_table_gene_protein(cursor, data):
    """
    Deze functie krijgt een lijst met dictionaries van data, checkt 
    door middel van een set met tuples er in of er dubbele waarden 
    zijn, en zorgt er ook gelijk voor dat de juiste waarden worden 
    gebruikt uit de dicts. Daarna wordt de gene_protein tabel van de 
    database met deze set gevuld.

    :param cursor: Dit object wordt gebruikt om de sql code te 
    runnen op de database server.
    :param data: lijst met dictionaries er in, met de data die in de
    database wordt gezet.
    :return None:
    """
    sql = """INSERT INTO GENE_PROTEIN
    VALUES(%s, %s)"""
    data_check = set()
    for item in data:
        data_check.add(tuple([item["ENSEMBL_gene_ID"], 
                              item["NCBI_prot_ID"]]))
    for line in data_check:
        cursor.execute(sql, line)
    print("Gene_protein table filled.")


def fill_table_pathway(cursor, data):
    """
    Deze functie krijgt een lijst met dictionaries van data, checkt 
    door middel van een set met tuples er in of er dubbele waarden 
    zijn, en zorgt er ook gelijk voor dat de juiste waarden worden 
    gebruikt uit de dicts. Daarna wordt de pathway tabel van de 
    database met deze set gevuld.

    :param cursor: Dit object wordt gebruikt om de sql code te 
    runnen op de database server.
    :param data: lijst met dictionaries er in, met de data die in de
    database wordt gezet.
    :return None:
    """
    sql = """INSERT INTO PATHWAY
    VALUES(%s, %s, %s)"""
    data_check = set()
    for item in data:
        data_check.add(tuple([item["pathway_ID"], item["pathway_name"], 
                              item["pathway_description"]]))
    for line in data_check:
        cursor.execute(sql, line)
    print("Pathway table filled.")


def fill_table_pathway_protein(cursor, data):
    """
    Deze functie krijgt een lijst met dictionaries van data, checkt 
    door middel van een set met tuples er in of er dubbele waarden 
    zijn, en zorgt er ook gelijk voor dat de juiste waarden worden 
    gebruikt uit de dicts. Daarna wordt de pathway_protein tabel van 
    de database met deze set gevuld.

    :param cursor: Dit object wordt gebruikt om de sql code te 
    runnen op de database server.
    :param data: lijst met dictionaries er in, met de data die in de
    database wordt gezet.
    :return None:
    """
    sql = """INSERT INTO PATHWAY_PROTEIN
    VALUES(%s, %s)"""
    data_check = set()
    for item in data:
        data_check.add(tuple([item["NCBI_prot_ID"], item["pathway_ID"]]))
    for line in data_check:
        cursor.execute(sql, line)
    print("Pathway_protein table filled.")


def fill_table_function(cursor, data):
    """
    Deze functie krijgt een lijst met dictionaries van data, checkt 
    door middel van een set met tuples er in of er dubbele waarden 
    zijn, en zorgt er ook gelijk voor dat de juiste waarden worden 
    gebruikt uit de dicts. Daarna wordt de function tabel van de 
    database met deze set gevuld.

    :param cursor: Dit object wordt gebruikt om de sql code te 
    runnen op de database server.
    :param data: lijst met dictionaries er in, met de data die in de
    database wordt gezet.
    :return None:
    """
    sql = """INSERT INTO FUNCTION
    VALUES(%s, %s)"""
    data_check = set()
    for item in data:
        data_check.add(tuple([item["prot_function_ID"], 
                              item["prot_function"]]))
    for line in data_check:
        cursor.execute(sql, line)
    print("Function table filled.")


def fill_table_function_protein(cursor, data, data_ids):
    """
    Deze functie krijgt twee lijsten met dictionaries van data, checkt 
    door middel van een set met tuples er in of er dubbele waarden 
    zijn, en zorgt er ook gelijk voor dat de juiste waarden worden 
    gebruikt uit de dicts. Daarna wordt de protein tabel van de 
    database met deze set gevuld.

    :param cursor: Dit object wordt gebruikt om de sql code te 
    runnen op de database server.
    :param data: lijst met dictionaries er in, met de data die in de
    database wordt gezet.
    :param data_ids: lijst met dictionaries er in, met de data die in 
    de database wordt gezet
    :return None:
    """
    sql = """INSERT INTO FUNCTION_PROTEIN
    VALUES(%s, %s)"""
    data_check = set()
    for item in data:
        _id = [fn_id["prot_function_ID"] for fn_id in data_ids if
               fn_id["prot_function"] == item["prot_function"]]
        data_check.add(tuple([item["NCBI_prot_ID"], _id[0]]))
    for line in data_check:
        cursor.execute(sql, line)
    print("Function_protein table filled.")


def fill_table_feature(cursor, data):
    """
    Deze functie krijgt een lijst met dictionaries van data, checkt 
    door middel van een set met tuples er in of er dubbele waarden 
    zijn, en zorgt er ook gelijk voor dat de juiste waarden worden 
    gebruikt uit de dicts. Daarna wordt de feature tabel van de 
    database met deze set gevuld.

    :param cursor: Dit object wordt gebruikt om de sql code te 
    runnen op de database server.
    :param data: lijst met dictionaries er in, met de data die in de
    database wordt gezet.
    :return None:
    """
    sql = """INSERT INTO FEATURE
    VALUES(%s, %s, %s, %s, %s)"""
    data_check = set()
    for item in data:
        data_check.add(tuple([item["NCBI_prot_ID"], item["feature_db_xref"], 
                             item["feature_type"], item["feature_position"], 
                             item["feature_note"]]))
    for line in data_check:
        cursor.execute(sql, line)
    print("Feature table filled.")


def parse_blast(file_list):
    """
    Deze functie krijgt alleen een lijst van bestand locaties mee, en
    geeft veschillende data uit deze bestanden terug in 3 sets. De 
    bestanden die deze functie inleest zijn de blast resultaten, die 
    eerder met het script 'blast_script.sh' zijn verkregen. Dit zijn 
    allemaal json bestanden, wat het makkelijk maakt om voor elk 
    brokstuk de juiste hits en informatie op te halen. Er zijn 3 
    verschillende sets die worden gevuld met tuples van informatie, 
    direct klaar om in de database gezet te worden (dus geen 
    duplicates). Elk van deze sets is voor een aparte tabel (zie 
    naamgeving van de sets)

    :param file_list: Lijst van bestandlocaties van json bestanden, 
    waar de blast resultaten in staan.
    :return (alignment_data, transcript_data, gene_data): Tuple van 
    3 sets met data erin, om de alignment, transcript_gene en gene 
    tabel te vullen.
    """

    alignment_data = set()
    gene_data = set()
    transcript_data = set()
    blast_db = []

    # data van blast DATABASE wordt ingelezen door middel van biopython
    path = "blast_db/pan_par_proteome.fa"
    for seq_record in SeqIO.parse(path, "fasta"):
        blast_db.append(seq_record)

    # resultaten worden per json bestand ingelezen
    for jsonpath in file_list:
        with open(jsonpath) as jsonfile:
            j = json.load(jsonfile)
        search = j['BlastOutput2']['report']['results']['search']
        try:
            if search["message"] == "No hits found":
                continue
        except Exception:
            pass

        # hier begint het parsen van de resultaten
        brokstuk_header = f">{search['query_title']}"
        query_len = search['query_len']

        for hit in search['hits']:
            # alleen eerste (beste) hit wordt gebruikt per bestand
            if hit['num'] > 1:
                break
                
            # transcript tabel data wordt verzameld
            transcript_id, description = \
                hit['description'][0]['title'].split(' ', 1)
            gene_id, desc_end = \
                description.split("gene:", 1)[-1].split(" ", 1)
            description = \
                "".join([description.split("gene:", 1)[0], desc_end])
            
            transcript_data.add(tuple([transcript_id, gene_id]))

            hsp = hit['hsps'][0]

            # gene tabel data wordt verzameld
            gene_value_list = []

            for line in gene_data:
                if line[0] == gene_id:
                    break
            else:
                gene_value_list.append(gene_id)
                try:
                    gene_name = \
                        description.split("gene_symbol:")[1].split(" ")[0]
                    gene_value_list.append(gene_name)
                except IndexError:
                    gene_value_list.append("unknown")
                gene_value_list.append(description)
                for seq_rec in blast_db:
                    if seq_rec.id == transcript_id:
                        gene_value_list.append(seq_rec.seq.__str__())
                gene_data.add(tuple(gene_value_list))

            # alignment tabel data wordt verzameld
            alignment_value_list = []

            alignment_value_list.append(brokstuk_header)
            alignment_value_list.append(transcript_id)
            alignment_value_list.append(hsp['align_len'])
            alignment_value_list.append(hsp['evalue'])
            alignment_value_list.append(hsp['bit_score'])
            alignment_value_list.append(
                round(hsp['identity'] / query_len * 100, 3))
            alignment_value_list.append(hsp['gaps'])
            alignment_value_list.append(
                hsp['align_len'] - hsp['identity'] - hsp['gaps'])
            alignment_value_list.append(hsp['hit_from'])
            alignment_value_list.append(hsp['hit_to'])
            alignment_data.add(tuple(alignment_value_list))
    return alignment_data, transcript_data, gene_data


def togows(gene_data):
    """
    Deze functie krijgt als enige argument een set met tuples van 
    data van de gene tabel, omdat deze data nodig is om andere data 
    op te halen (in deze data zitten namelijk de gene ID's). De manier 
    dat deze functie de benodigde data ophaalt, is door een website, 
    'togows.org' te querieen. Deze website is erg handig voor het 
    ophalen van data uit verschillende databases, en werkt ook vrij 
    simpel, aangezien je alles gewoon in json format terug krijgt. 
    Dit querieen wordt gedaan door middel van de 'requests' module. 
    er worden 3 verschillende 'base urls' gebruikt voor het querieen; 
    1 voor kegg-genes, 1 voor kegg-pathway en 1 voor ncbi-protein. 
    Deze 'base url' wordt steeds aangevuld met de juiste data ervoor. 
    Met de kegg-genes informatie wordt de protein data opgehaald. 
    Met de kegg-pathway informatie worden de pathway data en function 
    data opgehaald. En tot slot wordt met de ncbi-protein informatie de 
    feature data opgehaald. Deze opgehaalde data word allemaal opgeslagen 
    in verschillende lijsten van dictionaries.

    :param gene_data: Set met tuples van data nodig voor deze functie 
    om nog meer data op te halen.
    :return (protein_data, pathway_data, function_data, function_data_ids, \
        feature_data): Een tuple met meerdere lijsten waar dictionaries in 
    staan met data, om de resterende tabellen te kunnen vullen.
    """

    # eerste base url, voor protein data
    kegg_gene_url = "http://togows.org/entry/kegg-genes/ppad:{}.json"
    json_dict = {}
    for i in gene_data:
        if i[1] == "unknown":
            continue
        # data wordt opgehaald met requests.get().json()
        gene_req = requests.get(kegg_gene_url.format(i[1])).json()
        if gene_req:
            json_dict.update({
                i[0]: gene_req
            })
    protein_data = []
    for i, y in json_dict.items():
        dict_insert = {
            "ENSEMBL_gene_ID": i,
            "NCBI_prot_ID": y[0]["dblinks"]["NCBI-ProteinID"][0],
            "prot_name": y[0]["name"],
            "prot_sequence": y[0]["aaseq"],
            "pathways": y[0]["pathways"]
        }
        if dict_insert not in protein_data:
            protein_data.append(dict_insert)

    # tweede base_url, voor pathway data en function data
    kegg_pathway_url = "http://togows.org/entry/kegg-pathway/{}.json"
    pathway_data = []
    function_data = []
    func_list = set()

    for prot in protein_data:
        for pw_id, pw_name in prot["pathways"].items():
            # data wordt opgehaald met requests.get().json()
            pw_req = requests.get(kegg_pathway_url.format(pw_id)).json()
            pathway_desc = pw_req[0]["description"]
            if pathway_desc == "":
                pathway_desc = None
            pathway_data.append({
                "NCBI_prot_ID": prot["NCBI_prot_ID"],
                "pathway_ID": pw_id,
                "pathway_name": pw_name,
                "pathway_description": pathway_desc
            })
            for func in pw_req[0]["classes"]:
                dict_insert = {
                    "NCBI_prot_ID": prot["NCBI_prot_ID"],
                    "prot_function": func
                }
                func_list.add(func)
                if dict_insert not in function_data:
                    function_data.append(dict_insert)

    # function_data_ids verbindt de functies aan hun ID's
    function_data_ids = []
    count = 1
    for func in func_list:
        function_data_ids.append({
            "prot_function_ID": f"func_{count}",
            "prot_function": func
        })
        count += 1

    # derde base_url, voor feature data
    ncbi_protein_url = "http://togows.org/entry/ncbi-protein/{}.json"
    feature_data = []

    for item in protein_data:
        # data wordt opgehaald met requests.get().json()
        feat_req = requests.get(
            ncbi_protein_url.format(item["NCBI_prot_ID"])).json()
        for feat in feat_req[0]["features"]:
            note = None
            if "note" in feat:
                note = feat["note"][0]
            db_xref = None
            if "db_xref" in feat:
                db_xref = feat["db_xref"][0]
            feature_data.append({
                "NCBI_prot_ID": item["NCBI_prot_ID"],
                "feature_db_xref": db_xref,
                "feature_type": feat["feature"],
                "feature_position":
                    feat["position"].strip("order").strip("(").strip(")"),
                "feature_note": note
            })
    return protein_data, pathway_data, function_data, function_data_ids, \
        feature_data


def get_table_data():
    """
    Deze functie groepeert al het ophalen van de data door andere 
    functies aan te roepen, zodat hierna alle tabellen gevuld kunnen 
    worden. 

    :return (align_data, transcript_data, gene_data, protein_data, \
        pathway_data, function_data, function_data_ids, feature_data):
    Een tuple met meerdere sets waar tuples met data in zitten, en 
    lijsten waar dictionaries in staan met data, die allemaal worden 
    gebruikt om de tabellen te vullen.
    """

    # lijst van bestanden (de blast resultaten) wordt gemaakt
    directory = 'data/blast_results_json'
    file_list = []
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if "blast_results_" in filename:
            file_list.append(f)
    file_list.sort(key=lambda x: int(x.split("_")[-1].split(".")[0]))

    align_data, transcript_data, gene_data = parse_blast(file_list)
    protein_data, pathway_data, function_data, function_data_ids,\
        feature_data = togows(gene_data)
    return align_data, transcript_data, gene_data, protein_data, \
        pathway_data, function_data, function_data_ids, feature_data


def fill_all_tables(cursor):
    """
    Alle data wordt met get_table_data() opgehaald, en alle tabellen 
    worden gevuld.

    :param cursor: Dit object wordt gebruikt om de sql code te 
    runnen op de database server.
    :return None:
    """
    align_data, transcript_data, gene_data, protein_data, pathway_data, \
        function_data, function_data_ids, feature_data = get_table_data()
    fill_table_brokstuk(cursor)
    fill_table_gene(cursor, gene_data)
    fill_table_transcript_gene(cursor, transcript_data)
    fill_table_alignment(cursor, align_data)
    fill_table_protein(cursor, protein_data)
    fill_table_gene_protein(cursor, protein_data)
    fill_table_pathway(cursor, pathway_data)
    fill_table_pathway_protein(cursor, pathway_data)
    fill_table_function(cursor, function_data_ids)
    fill_table_function_protein(cursor, function_data, function_data_ids)
    fill_table_feature(cursor, feature_data)
    print("All tables filled!")
