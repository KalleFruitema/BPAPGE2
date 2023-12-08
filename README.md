# BPAPGE2

BPAPGE project group 2

## Modules

Voordat dit programma gerunned wordt, check of de benodigde modules geinstalleerd zijn op uw versie van python (op de bioserver zijn deze modules al geinstalleerd). De benodigde modules zijn:

- psycopg2

- biopython

- requests

Zie ook requirements.txt

## Instructies

Instructies voor wanneer er alleen nog maar scripts zijn (en seq2.fa), en de blast dus nog gerunned moet worden:

- Stap 1: Open bash

- Stap 2: Run main.sh (command= "./main.sh")

- Stap 3: dat was het :D de database is nu gemaakt en gevuld.

## Alternatieve instructies

Voor wanneer de blast query al gerunned is (json files in blast_db/blast_json bestaan), en je alleen nog de database moet aanmaken en vullen:

- Stap 1: Open bash

- Stap 2: Run main.py (command= "python3 code/main.py")

- Stap 3: klaar

Voor wanneer je alleen de json blast bestanden wilt aanmaken:

- Stap 1: Open bash

- Stap 2: Run blast_script.sh (command= "./code/blast_script.sh")

- Stap 3: klaar
