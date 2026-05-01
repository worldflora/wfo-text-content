# Geographic data extracted from WCVP

This uses data downloaded from this URL 

https://sftp.kew.org/pub/data-repositories/WCVP/wcvp_dwca.zip

It is joined to the name matched version of WCVP in a MySQL database 

## TDWG Level 3 "Botanical Countries"

The TDWG Level 3 regions can be extracted directly from the downloaded file as this is the level Kew have scored the taxa to.

## ISO Alpha 2 Countries

Some of the TDWG Level 3 codes correspond to ISO countries (e.g. Zimbabwe), others are unambiguously part of ISO countries (e.g. the states of the United States of America). A mapping file was prepared (a copy is in the raw directory) mapping between Level 3 codes and countries that allowed distributions by country to be extracted from WCVP. This is not a comprehensive list as there is ambiguity in some of the Level 3 areas. It does provide useful data where matches can be made unambiguously though.

