#!/bin/bash

# Date: 8/12/2023
# Author: Kalle Fruitema
# Dit script runt eerst de blast door middel van code/blast_script.sh
# en runt dan code/main.py om de sql database aan te maken en te vullen.

# Usage: $ ./main.sh

# blast wordt uitgevoerd
./code/blast_script.sh

# database wordt gemaakt en gevuld
python3 code/main.py
