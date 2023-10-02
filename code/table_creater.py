def create_table_brokstuk(cursor):
    sql = """CREATE TABLE BROKSTUK(
    brokstuk_header VARCHAR(255) NOT NULL UNIQUE,
    brokstuk_sequence TEXT NOT NULL UNIQUE,

    CONSTRAINT pk_brokstuk_header
    PRIMARY KEY(brokstuk_header)
    )"""
    cursor.execute(sql)
    print("Brokstuk table created!")


def create_table_alignment(cursor):
    sql = """CREATE TABLE ALIGNMENT(
    brokstuk_header VARCHAR(255) NOT NULL,
    alignment_ID INTEGER NOT NULL,
    ENSEMBL_gene_ID VARCHAR(255) NOT NULL,
    alignment_length INTEGER NOT NULL,
    e_value DOUBLE PRECISION NOT NULL,
    bit_score INTEGER NOT NULL,
    percentage_identity NUMERIC(6,3) NOT NULL,
    gaps INTEGER NOT NULL,
    mismatches INTEGER NOT NULL,
    startpos_hit INTEGER NOT NULL,
    endpos_hit INTEGER NOT NULL,

    CONSTRAINT fk_brokstuk_header
    FOREIGN KEY(brokstuk_header)
    REFERENCES BROKSTUK(brokstuk_header),

    CONSTRAINT fk_ENSEMBL_gene_ID
    FOREIGN KEY(ENSEMBL_gene_ID)
    REFERENCES GENE(ENSEMBL_gene_ID)
    )"""
    cursor.execute(sql)
    print("Alignment table created!")


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


def create_table_gene_protein(cursor):
    sql = """CREATE TABLE GENE_PROTEIN(
    ENSEMBL_gene_ID VARCHAR(255) NOT NULL,
    NCBI_prot_ID VARCHAR(255) NOT NULL,

    CONSTRAINT fk_ENSEMBL_gene_ID
    FOREIGN KEY(ENSEMBL_gene_ID)
    REFERENCES GENE(ENSEMBL_gene_ID),

    CONSTRAINT fk_NCBI_prot_ID
    FOREIGN KEY(NCBI_prot_ID)
    REFERENCES PROTEIN(NCBI_prot_ID)
    )"""
    cursor.execute(sql)
    print("Gene_protein table created!")


def create_table_pathway(cursor):
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
    sql = """CREATE TABLE PATHWAY_PROTEIN(
    NCBI_prot_ID VARCHAR(255) NOT NULL,
    pathway_ID VARCHAR(255) NOT NULL,

    CONSTRAINT fk_NCBI_prot_ID
    FOREIGN KEY(NCBI_prot_ID)
    REFERENCES PROTEIN(NCBI_prot_ID),

    CONSTRAINT fk_pathway_id
    FOREIGN KEY(pathway_ID)
    REFERENCES PATHWAY(pathway_ID)
    )"""
    cursor.execute(sql)
    print("Pathway_protein table created!")


def create_table_protein(cursor):
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
    sql = """CREATE TABLE FUNCTION_PROTEIN(
    NCBI_prot_ID VARCHAR(255) NOT NULL,
    prot_function_ID VARCHAR(255) NOT NULL,

    CONSTRAINT fk_NCBI_prot_ID
    FOREIGN KEY(NCBI_prot_ID)
    REFERENCES PROTEIN(NCBI_prot_ID),

    CONSTRAINT fk_prot_function_ID
    FOREIGN KEY(prot_function_ID)
    REFERENCES FUNCTION(prot_function_ID)
    )"""
    cursor.execute(sql)
    print("Function_protein table created!")


def create_table_function(cursor):
    sql = """CREATE TABLE FUNCTION(
    prot_function_ID VARCHAR(255) NOT NULL UNIQUE,
    prot_function TEXT NOT NULL UNIQUE,

    CONSTRAINT pk_prot_function_ID
    PRIMARY KEY(prot_function_ID)
    )"""
    cursor.execute(sql)
    print("Function table created!")


def create_table_spliced_gene(cursor):
    sql = """CREATE TABLE SPLICED_GENE(
    ENSEMBL_gene_ID VARCHAR(255) NOT NULL UNIQUE,
    splice_gene_ID VARCHAR(255) NOT NULL UNIQUE,
    start_intron INTEGER NOT NULL,
    eind_intron INTEGER NOT NULL,
    NCBI_prot_ID VARCHAR(255) NOT NULL,

    CONSTRAINT fk_ENSEMBL_gene_ID
    FOREIGN KEY(ENSEMBL_gene_ID)
    REFERENCES GENE(ENSEMBL_gene_ID),

    CONSTRAINT fk_NCBI_prot_ID
    FOREIGN KEY(NCBI_prot_ID)
    REFERENCES PROTEIN(NCBI_prot_ID)
    )"""
    cursor.execute(sql)
    print("Spliced_gene table created!")
