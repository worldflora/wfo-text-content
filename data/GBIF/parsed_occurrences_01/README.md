# Parsed GBIF global plant occurrence data 1.0 Plus

This is based on a data set produced by Pablo Hendrigo Alves de Melo, Nadia Bystriakova, Alexandre Monro.

Unique collection events (28,492,644) of all vascular plant specimens preserved in herbarium from the Biodiversity Information Facility (GBIF). The occurrences were processed by the ParseGBIF package workflow (https://github.com/pablopains/parseGBIF; https://doi.org/10.1038/s41598-024-56158-3), designed to verify and standardize scientific names of species according to the World Checklist of Vascular Plants taxonomic backbone and to analyze duplicate records in 'unique collection events'. This dataset represents 'unique collection events' of useable data with successfully verified geographic coordinates.

The raw data is available at the Figshare website here: https://figshare.com/articles/dataset/Parsed_GBIF_global_plant_occurrence_data_1_0_Plus/27122574
It is far too big for GitHub even when zipped up.

Subsequent releases of this data can be parsed in a similar way when they become available.

## Country data reverse geocode

Here we have extracted the count of specimens per ISO country (ISO3166) based on the set of polygons used to draw the maps in the portal. The polygons are in the raw/country_files folder.

Reverse geocoding is done using the MySQL geospatial indexing.

The specimens are named according to Kew's WCVP data set releasd 2026-01-07 (https://sftp.kew.org/pub/data-repositories/WCVP/). We maintain a mapping between WCVP plant name IDs and WFO IDs and a copy of this mapping is included in the raw folder although the scripts run against our local WCVP copy table.


## Global zones

It is computationally straight forward to attribute geospatial points to zones that are defined as simple latitudinal bands or longitudinal segments on the earth's surface. These zones can be chosen to align with useful categories people may wish to query botanical data on. They can be particularly useful when combined. These are not biologically perfect  (it would be nice to have one run through the Wallace Line for example) but their usefulness far exceeds the cost of scoring data to them. Here we define: 

1. __Tropical Band:__ Plants occurring above -23.4° and below +23.4° latitude.
1. __Northern Temperate Band:__ Plants occurring above +23.4° and below +60° latitude.
1. __Southern Temperate Band:__ Plants occurring above -60° and below -23.4° latitude.
1. __Temperate Bands:__ Plants occurring in either Northern or Southern temperate zones.
1. __Arctic Band:__ Plants occurring above +60° latitude.
1. __Antarctic Band:__ Plants occurring below -60° latitude.
1. __Polar Bands:__ Plants occurring in Arctic or Antarctic regions.
1. __Western Segment:__ The zone from -30° to -170° longitude. This is from just West of Iceland to approximately the international date line and includes North America, South America and Greenland.
1. __Afro-European Segment:__ From -30° to +60° longitude. This is from mid Atlantic to the tip of Oman and roughly lines up with the Ural Mountains. It includes the whole of Europe (including European Russia) and the whole of Africa and West Asia.
1. __South Asian Segment:__ From +60° to +95° longitude. Including the *stan countries, India and the nearly the whole of the Himalaya as well as central Russia.
1. __East Asian Segment:__ From +95° to -170° longitude. It includes the countries usually thought of as East Asia (China, Japan, Mongolia, North Korea, South Korea, and Taiwan) and also those of Southeast Asia (Cambodia, Laos, and Vietnam) and Oceania (Australasia, Melanesia, Micronesia, and Polynesia). All these countries falling in the same longitudinal section of the earth but divisible by the latitudinal bands they occur in. e.g. Combined with the Tropical Band it approximates to Souteast Asia or with the Southern Temperate Band to approximate Oceania. 

The reverse_geocode_by_zone.php script creates a MySQL table with the taxa by zones from the points data file. The export_zone_csv_files.php script generates (big) CSV zip files for each of the zones.

