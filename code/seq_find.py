import requests


def get_seq(ids):
    full_file = ""
    for org, id in ids:
        if org in [">Alligator", ">Vogelbekdier", ">Melano"]:
            togows = "http://togows.org/entry/ebi-uniprot/{}.fasta"
        else:
            togows = "http://togows.org/entry/ncbi-protein/{}.fasta"
        f = requests.get(togows.format(id)).text
        full_file += f
    with open("results/orthologe_sequenties.fa", "w+") as fa_file:
        fa_file.write(full_file)


def main():
    with open("results/sequenties_hoogste_identity.txt") as id_file:
        ids = id_file.read().strip().split("\n")
    for i, y in enumerate(ids):
        ids[i] = y.strip().split(" ")
    get_seq(ids)


if __name__ == "__main__":
    main()