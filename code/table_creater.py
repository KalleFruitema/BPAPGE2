"""
File: table_creater.py
Author: Kalle Fruitema
Date: 08/12/2023
Description: Maakt alle tabellen aan.
Version: Python v3.12.0
"""


def create_table_brokstuk(cursor):
    """
    Maakt de brokstuk tabel aan met de juiste waarden,
    datatypen van de waarden en constraints.

    :param cursor: Dit wordt gebruikt om de sql code te runnen
    op de database server
    :return None:
    """
    sql = """CREATE TABLE BROKSTUK(
    brokstuk_header VARCHAR(255) NOT NULL UNIQUE,
    brokstuk_sequence TEXT NOT NULL,
    
    CONSTRAINT pk_brokstuk_header
    PRIMARY KEY(brokstuk_header)
    )"""
    cursor.execute(sql)
    print("Brokstuk table created.")


def create_table_alignment(cursor):
    """
    Maakt de alignment tabel aan met de juiste waarden,
    datatypen van de waarden en constraints.

    :param cursor: Dit wordt gebruikt om de sql code te runnen
    op de database server
    :return None:
    """
    sql = """CREATE TABLE ALIGNMENT(
    brokstuk_header VARCHAR(255) NOT NULL,
    ensembl_transcript_id VARCHAR(255) NOT NULL,
    alignment_length INTEGER NOT NULL,
    e_value DOUBLE PRECISION NOT NULL,
    bit_score INTEGER NOT NULL,
    percentage_identity NUMERIC(6,3) NOT NULL,
    gaps INTEGER NOT NULL,
    mismatches INTEGER NOT NULL,
    startpos_hit INTEGER NOT NULL,
    endpos_hit INTEGER NOT NULL,

    CONSTRAINT pk_alignment_brokstuk_header
    PRIMARY KEY(brokstuk_header),

    CONSTRAINT fk_brokstuk_header
    FOREIGN KEY(brokstuk_header)
    REFERENCES BROKSTUK(brokstuk_header),

    CONSTRAINT fk_ensembl_transcript_id
    FOREIGN KEY(ensembl_transcript_id)
    REFERENCES TRANSCRIPT_GENE(ensembl_transcript_id)
    )"""
    cursor.execute(sql)
    print("Alignment table created.")


def create_table_transcript_gene(cursor):
    """
    Maakt de transcript_gene tabel aan met de juiste waarden, 
    datatypen van de waarden en constraints.
    
    :param cursor: Dit object wordt gebruikt om de sql code te 
    runnen op de database server.
    :return None: 
    """
    sql = """CREATE TABLE TRANSCRIPT_GENE(
    ensembl_transcript_id VARCHAR(255) NOT NULL UNIQUE,
    ensembl_gene_id VARCHAR(255) NOT NULL,

    CONSTRAINT pk_ensembl_transcript_id
    PRIMARY KEY(ensembl_transcript_id),

    CONSTRAINT fk_ensembl_gene_id
    FOREIGN KEY(ensembl_gene_id)
    REFERENCES GENE(ensembl_gene_id)
    )"""
    cursor.execute(sql)
    print("Transcript_gene table created.")


def create_table_gene(cursor):
    """
    Maakt de gene tabel aan met de juiste waarden, 
    datatypen van de waarden en constraints.
    
    :param cursor: Dit object wordt gebruikt om de sql code te 
    runnen op de database server.
    :return None: 
    """
    sql = """CREATE TABLE GENE(
    ensembl_gene_id VARCHAR(255) NOT NULL UNIQUE,
    gene_name VARCHAR(255) NOT NULL,
    gene_description VARCHAR(255) NULL,
    gene_scaffold VARCHAR(255) NULL,
    gene_sequence TEXT NOT NULL,

    CONSTRAINT pk_ensembl_gene_id
    PRIMARY KEY(ensembl_gene_id)
    )"""
    cursor.execute(sql)
    print("Gene table created.")


def create_table_gene_protein(cursor):
    """
    Maakt de gene_protein tabel aan met de juiste waarden, 
    datatypen van de waarden en constraints.
    
    :param cursor: Dit object wordt gebruikt om de sql code te 
    runnen op de database server.
    :return None: 
    """
    sql = """CREATE TABLE GENE_PROTEIN(
    ensembl_gene_id VARCHAR(255) NOT NULL,
    ncbi_prot_id VARCHAR(255) NOT NULL,

    CONSTRAINT fk_ensembl_gene_id
    FOREIGN KEY(ensembl_gene_id)
    REFERENCES GENE(ensembl_gene_id),

    CONSTRAINT fk_ncbi_prot_id
    FOREIGN KEY(ncbi_prot_id)
    REFERENCES PROTEIN(ncbi_prot_id),

    CONSTRAINT ck_GENE_PROTEIN
    PRIMARY KEY(ensembl_gene_id, ncbi_prot_id)
    )"""
    cursor.execute(sql)
    print("Gene_protein table created.")


def create_table_pathway(cursor):
    """
    Maakt de pathway tabel aan met de juiste waarden, 
    datatypen van de waarden en constraints.
    
    :param cursor: Dit object wordt gebruikt om de sql code te 
    runnen op de database server.
    :return None: 
    """
    sql = """CREATE TABLE PATHWAY(
    pathway_id VARCHAR(255) NOT NULL UNIQUE,
    pathway_name VARCHAR(255) NOT NULL,
    pathway_description TEXT NULL,

    CONSTRAINT pk_pathway_id
    PRIMARY KEY(pathway_id) 
    )"""
    cursor.execute(sql)
    print("Pathway table created.")


def create_table_pathway_protein(cursor):
    """
    Maakt de pathway_protein tabel aan met de juiste waarden, 
    datatypen van de waarden en constraints.
    
    :param cursor: Dit object wordt gebruikt om de sql code te 
    runnen op de database server.
    :return None: 
    """
    sql = """CREATE TABLE PATHWAY_PROTEIN(
    ncbi_prot_id VARCHAR(255) NOT NULL,
    pathway_id VARCHAR(255) NOT NULL,

    CONSTRAINT fk_ncbi_prot_id
    FOREIGN KEY(ncbi_prot_id)
    REFERENCES PROTEIN(ncbi_prot_id),

    CONSTRAINT fk_pathway_id
    FOREIGN KEY(pathway_id)
    REFERENCES PATHWAY(pathway_id),

    CONSTRAINT ck_PATHWAY_PROTEIN
    PRIMARY KEY(ncbi_prot_id, pathway_id)
    )"""
    cursor.execute(sql)
    print("Pathway_protein table created.")


def create_table_protein(cursor):
    """
    Maakt de protein tabel aan met de juiste waarden, 
    datatypen van de waarden en constraints.
    
    :param cursor: Dit object wordt gebruikt om de sql code te 
    runnen op de database server.
    :return None: 
    """
    sql = """CREATE TABLE PROTEIN(
    ncbi_prot_id VARCHAR(255) NOT NULL UNIQUE,
    prot_name VARCHAR(255) NOT NULL,
    prot_sequence TEXT NOT NULL,

    CONSTRAINT pk_ncbi_prot_id
    PRIMARY KEY(ncbi_prot_id)
    )"""
    cursor.execute(sql)
    print("Protein table created.")


def create_table_function_protein(cursor):
    """
    Maakt de function_protein tabel aan met de juiste waarden, 
    datatypen van de waarden en constraints.
    
    :param cursor: Dit object wordt gebruikt om de sql code te 
    runnen op de database server.
    :return None: 
    """
    sql = """CREATE TABLE FUNCTION_PROTEIN(
    ncbi_prot_id VARCHAR(255) NOT NULL,
    prot_function_id VARCHAR(255) NOT NULL,

    CONSTRAINT fk_ncbi_prot_id
    FOREIGN KEY(ncbi_prot_id)
    REFERENCES PROTEIN(ncbi_prot_id),

    CONSTRAINT fk_prot_function_id
    FOREIGN KEY(prot_function_id)
    REFERENCES FUNCTION(prot_function_id),

    CONSTRAINT ck_FUNCTION_PROTEIN
    PRIMARY KEY(ncbi_prot_id, prot_function_id)
    )"""
    cursor.execute(sql)
    print("Function_protein table created.")


def create_table_function(cursor):
    """
    Maakt de function tabel aan met de juiste waarden, 
    datatypen van de waarden en constraints.
    
    :param cursor: Dit object wordt gebruikt om de sql code te 
    runnen op de database server.
    :return None: 
    """
    sql = """CREATE TABLE FUNCTION(
    prot_function_id VARCHAR(255) NOT NULL UNIQUE,
    prot_function TEXT NOT NULL UNIQUE,

    CONSTRAINT pk_prot_function_id
    PRIMARY KEY(prot_function_id)
    )"""
    cursor.execute(sql)
    print("Function table created.")


def create_table_feature(cursor):
    """
    Maakt de feature tabel aan met de juiste waarden, 
    datatypen van de waarden en constraints.
    
    :param cursor: Dit object wordt gebruikt om de sql code te 
    runnen op de database server.
    :return None: 
    """
    sql = """CREATE TABLE FEATURE(
    feature_id INTEGER NOT NULL UNIQUE,
    ncbi_prot_id VARCHAR(255) NOT NULL,
    feature_db_xref VARCHAR(255) NULL,
    feature_type VARCHAR(255) NOT NULL,
    feature_note TEXT NULL,
    feature_length INTEGER NOT NULL,
    skipped_positions BOOLEAN NOT NULL,
    feature_positions INTEGER ARRAY NOT NULL,
    
    CONSTRAINT pk_feature_id
    PRIMARY KEY(feature_id),

    CONSTRAINT fk_ncbi_prot_id
    FOREIGN KEY(ncbi_prot_id)
    REFERENCES PROTEIN(ncbi_prot_id)
    )"""
    cursor.execute(sql)
    print("Feature table created.")


def create_all_tables(cursor):
    """
    Maakt alle tabellen aan in 1 functie, zodat deze vanuit de
    main makkelijk aangeroepen kan worden.

    :param cursor: Dit object wordt gebruikt om de sql code te 
    runnen op de database server.
    :return None: 
    """
    create_table_brokstuk(cursor)
    create_table_gene(cursor)
    create_table_transcript_gene(cursor)
    create_table_alignment(cursor)
    create_table_function(cursor)
    create_table_pathway(cursor)
    create_table_protein(cursor)
    create_table_pathway_protein(cursor)
    create_table_function_protein(cursor)
    create_table_gene_protein(cursor)
    create_table_feature(cursor)
    print("All tables created.")
