Downloaded Redlist version 2026_1

There are 78329 record in the csv.
_internalTaxonId_ used to map WFOIDs across from 2025_2.

1926 new assessments in 2026_01. 2 names added to WFO.
722 rows have not matched and do not have a WFO.
61 appear to be unpublished. 

CSV was added to an SQLite DB. Query to extract a csv for each Redlist Category given in script folder.

|redlistCategory| count|
|----------------|-------|
|Least Concern |	36095|
|Endangered |	12845|
|Vulnerable |	10570|
|Critically Endangered |	6469|
|Data Deficient |	6275|
|Near Threatened |	4620|
|Lower Risk/near threatened |	256|
|Extinct |	143|
|Lower Risk/least concern |	116|
|Lower Risk/conservation dependent |	101|
|Extinct in the Wild	|46|

Lower Risk assessments have been excluded. 

2026_01 assessments linked to Fyllo - August 2026.

**TO DO**

- Try to match remaining names.

--------------------------------------------------------------------------------------------------------------

Downloaded Redlist version 2025_2.

There are 76441 rows in the CSV. 
These were name matched. 

710 rows have not matched and do not have a WFO.

CSV was added to an SQLite DB. Query to extract a csv for each Redlist Category given in script folder.

|redlistCategory | count|
|----------------|-------|
|Least Concern | 35518|
|Endangered | 12635|
|Vulnerable | 10532|
|Critically Endangered | 6391|
|Data Deficient | 6214|
|Near Threatened | 4466|
|Lower Risk/near threatened | 270|
|Extinct | 136|
|Lower Risk/least concern | 125|
|Lower Risk/conservation dependent | 108|
|Extinct in the Wild | 46|

Lower Risk assessments have been excluded. 

To Do: 
 - missing WFO IDs need added to cover additional
 - Use Cross Ref API to get references for all the assessments.
