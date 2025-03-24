# Link-outs for names in the NCBI taxonomy


## scripts/download_and_extract.php

-  If new_taxdump.zip is not present in the raw/ directory the script will download it from ncbi at this address (https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/new_taxdump/new_taxdump.zip).
- There is a .ignore file in the raw/ directory to prevent new_taxdump.zip being checked into git as it is rather big (140MB) and we only want a subset of it.
- Once new_taxdump.zip is downloaded the script will work through rankedlineage.dmp within the zip archive and write it out to working/rankedlineage.csv.zip
    - The NCBI .dmp files are in weird formats and we need to get it into a standard CSV format
    - The file contains all of life and we just want the plants so irrelevant lines are discared.


## scripts/generate_out_csv.php

- Takes the CSV file created by the above script and generates out/ncbi_taxonomy_matched.csv.zip suitable for import to the faceting server
- Will name match based on the string in the second column of rankedlineage.csv.zip
- Keeps a cash.csv in matching_cache.csv of NCBI to WFO IDs to prevent having to name match the same name one twice.
- We use zip files for space saving in github. You will need to unzip rankedlineage.csv.zip but don't check the zipped up version into github (it is in a .gitignore anyhow)


