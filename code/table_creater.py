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
    brokstuk_sequence TEXT NOT NULL UNIQUE,

    CONSTRAINT pk_brokstuk_header
    PRIMARY KEY(brokstuk_header)
    )"""
    cursor.execute(sql)
    print("Brokstuk table created!")


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
    ENSEMBL_transcript_ID VARCHAR(255) NOT NULL,
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

    CONSTRAINT fk_ENSEMBL_transcript_ID
    FOREIGN KEY(ENSEMBL_transcript_ID)
    REFERENCES TRANSCRIPT_GENE(ENSEMBL_transcript_ID)
    )"""
    cursor.execute(sql)
    print("Alignment table created!")


def create_table_transcript_gene(cursor):
    """
    Maakt de transcript_gene tabel aan met de juiste waarden, 
    datatypen van de waarden en constraints.
    
    :param cursor: Dit object wordt gebruikt om de sql code te 
    runnen op de database server.
    :return None: 
    """
    sql = """CREATE TABLE TRANSCRIPT_GENE(
    ENSEMBL_transcript_ID VARCHAR(255) NOT NULL UNIQUE,
    ENSEMBL_gene_ID VARCHAR(255) NOT NULL,

    CONSTRAINT pk_ENSEMBL_transcript_ID
    PRIMARY KEY(ENSEMBL_transcript_ID),

    CONSTRAINT fk_ENSEMBL_gene_ID
    FOREIGN KEY(ENSEMBL_gene_ID)
    REFERENCES GENE(ENSEMBL_gene_ID)
    )"""
    cursor.execute(sql)
    print("Transcript_gene table created!")


def create_table_gene(cursor):
    """
    Maakt de gene tabel aan met de juiste waarden, 
    datatypen van de waarden en constraints.
    
    :param cursor: Dit object wordt gebruikt om de sql code te 
    runnen op de database server.
    :return None: 
    """
    sql = """CREATE TABLE GENE(
    ENSEMBL_gene_ID VARCHAR(255) NOT NULL UNIQUE,
    gene_name VARCHAR(255) NOT NULL,
    gene_description TEXT,
    gene_sequence TEXT NOT NULL UNIQUE,

    CONSTRAINT pk_ENSEMBL_gene_ID
    PRIMARY KEY(ENSEMBL_gene_ID)
    )"""
    cursor.execute(sql)
    print("Gene table created!")


def create_table_gene_protein(cursor):
    """
    Maakt de gene_protein tabel aan met de juiste waarden, 
    datatypen van de waarden en constraints.
    
    :param cursor: Dit object wordt gebruikt om de sql code te 
    runnen op de database server.
    :return None: 
    """
    sql = """CREATE TABLE GENE_PROTEIN(
    ENSEMBL_gene_ID VARCHAR(255) NOT NULL,
    NCBI_prot_ID VARCHAR(255) NOT NULL,

    CONSTRAINT fk_ENSEMBL_gene_ID
    FOREIGN KEY(ENSEMBL_gene_ID)
    REFERENCES GENE(ENSEMBL_gene_ID),

    CONSTRAINT fk_NCBI_prot_ID
    FOREIGN KEY(NCBI_prot_ID)
    REFERENCES PROTEIN(NCBI_prot_ID),

    CONSTRAINT ck_GENE_PROTEIN
    PRIMARY KEY(ENSEMBL_gene_ID, NCBI_prot_ID)
    )"""
    cursor.execute(sql)
    print("Gene_protein table created!")


def create_table_pathway(cursor):
    """
    Maakt de pathway tabel aan met de juiste waarden, 
    datatypen van de waarden en constraints.
    
    :param cursor: Dit object wordt gebruikt om de sql code te 
    runnen op de database server.
    :return None: 
    """
    sql = """CREATE TABLE PATHWAY(
    pathway_ID VARCHAR(255) NOT NULL UNIQUE,
    pathway_name VARCHAR(255) NOT NULL,
    pathway_description TEXT NULL,

    CONSTRAINT pk_pathway_ID
    PRIMARY KEY(pathway_ID) 
    )"""
    cursor.execute(sql)
    print("Pathway table created!")


def create_table_pathway_protein(cursor):
    """
    Maakt de pathway_protein tabel aan met de juiste waarden, 
    datatypen van de waarden en constraints.
    
    :param cursor: Dit object wordt gebruikt om de sql code te 
    runnen op de database server.
    :return None: 
    """
    sql = """CREATE TABLE PATHWAY_PROTEIN(
    NCBI_prot_ID VARCHAR(255) NOT NULL,
    pathway_ID VARCHAR(255) NOT NULL,

    CONSTRAINT fk_NCBI_prot_ID
    FOREIGN KEY(NCBI_prot_ID)
    REFERENCES PROTEIN(NCBI_prot_ID),

    CONSTRAINT fk_pathway_id
    FOREIGN KEY(pathway_ID)
    REFERENCES PATHWAY(pathway_ID),

    CONSTRAINT ck_PATHWAY_PROTEIN
    PRIMARY KEY(NCBI_prot_ID, pathway_ID)
    )"""
    cursor.execute(sql)
    print("Pathway_protein table created!")


def create_table_protein(cursor):
    """
    Maakt de protein tabel aan met de juiste waarden, 
    datatypen van de waarden en constraints.
    
    :param cursor: Dit object wordt gebruikt om de sql code te 
    runnen op de database server.
    :return None: 
    """
    sql = """CREATE TABLE PROTEIN(
    NCBI_prot_ID VARCHAR(255) NOT NULL UNIQUE,
    prot_name VARCHAR(255) NOT NULL,
    prot_sequence TEXT NOT NULL UNIQUE,

    CONSTRAINT pk_NCBI_prot_ID
    PRIMARY KEY(NCBI_prot_ID)
    )"""
    cursor.execute(sql)
    print("Protein table created!")


def create_table_function_protein(cursor):
    """
    Maakt de function_protein tabel aan met de juiste waarden, 
    datatypen van de waarden en constraints.
    
    :param cursor: Dit object wordt gebruikt om de sql code te 
    runnen op de database server.
    :return None: 
    """
    sql = """CREATE TABLE FUNCTION_PROTEIN(
    NCBI_prot_ID VARCHAR(255) NOT NULL,
    prot_function_ID VARCHAR(255) NOT NULL,

    CONSTRAINT fk_NCBI_prot_ID
    FOREIGN KEY(NCBI_prot_ID)
    REFERENCES PROTEIN(NCBI_prot_ID),

    CONSTRAINT fk_prot_function_ID
    FOREIGN KEY(prot_function_ID)
    REFERENCES FUNCTION(prot_function_ID),

    CONSTRAINT ck_FUNCTION_PROTEIN
    PRIMARY KEY(NCBI_prot_ID, prot_function_ID)
    )"""
    cursor.execute(sql)
    print("Function_protein table created!")


def create_table_function(cursor):
    """
    Maakt de function tabel aan met de juiste waarden, 
    datatypen van de waarden en constraints.
    
    :param cursor: Dit object wordt gebruikt om de sql code te 
    runnen op de database server.
    :return None: 
    """
    sql = """CREATE TABLE FUNCTION(
    prot_function_ID VARCHAR(255) NOT NULL UNIQUE,
    prot_function TEXT NOT NULL UNIQUE,

    CONSTRAINT pk_prot_function_ID
    PRIMARY KEY(prot_function_ID)
    )"""
    cursor.execute(sql)
    print("Function table created!")


def create_table_feature(cursor):
    """
    Maakt de feature tabel aan met de juiste waarden, 
    datatypen van de waarden en constraints.
    
    :param cursor: Dit object wordt gebruikt om de sql code te 
    runnen op de database server.
    :return None: 
    """
    sql = """CREATE TABLE FEATURE(
    NCBI_prot_ID VARCHAR(255) NOT NULL,
    feature_db_xref VARCHAR(255) NULL,
    feature_type VARCHAR(255) NOT NULL,
    feature_position VARCHAR(255) NOT NULL,
    feature_note TEXT NULL,

    CONSTRAINT fk_NCBI_prot_ID
    FOREIGN KEY(NCBI_prot_ID)
    REFERENCES PROTEIN(NCBI_prot_ID)
    )"""
    cursor.execute(sql)
    print("Feature table created!")


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
    print("All tables created!")
