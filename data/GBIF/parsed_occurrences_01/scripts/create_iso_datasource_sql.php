<?php

/*
    This is a run once script to generated SQL Insert statements to add 
    data sources for countries
*/
// get the database connection.
require_once('../../../../../wfo_fyllo_secrets.php');
$mysqli = new mysqli($db_host, $db_user, $db_password, $db_database); 

$response = $mysqli->query("SELECT `id`, `code`, `name` FROM wfo_facets.facet_values where facet_id = 1");
$facet_values = $response->fetch_all(MYSQLI_ASSOC);
$response->close();

print_r($facet_values);


$out = fopen('../working/iso_insert.sql', 'w');
foreach($facet_values as $fv){

    // check the file exists
    $local_files = glob("../out/countries/{$fv['code']}.csv.zip");
    if(count($local_files) != 1) continue;

    // skip the ones we have already done
    if(in_array($fv['code'], array(
        'AF',
        'AL',
        'DZ',
        'AD',
        'AO',
        'AR',
        'AM',
        'AU'
    ))) continue;

    $remote_path = "data/GBIF/parsed_occurrences_01/out/countries/{$fv['code']}.csv.zip";
    
    $name = $mysqli->real_escape_string("{$fv['name']} from parsed GBIF occurrence data.");
    $description = $mysqli->real_escape_string("This is based on a data set produced by Pablo Hendrigo Alves de Melo, Nadia Bystriakova and Alexandre Monro. Unique collection events (28,492,644) of all vascular plant specimens preserved in herbarium from the Biodiversity Information Facility (GBIF). The occurrences were processed by the ParseGBIF package workflow (https://github.com/pablopains/parseGBIF; https://doi.org/10.1038/s41598-024-56158-3), designed to verify and standardize scientific names of species according to the World Checklist of Vascular Plants taxonomic backbone and to analyze duplicate records in 'unique collection events'. This dataset represents 'unique collection events' of useable data with successfully verified geographic coordinates. The raw data is available at the Figshare website here: https://figshare.com/articles/dataset/Parsed_GBIF_global_plant_occurrence_data_1_0_Plus/27122574 It is far too big for GitHub even when zipped up. These specimen records were matched via their Kew-WCVP name identifiers and reverse geocoded to country polygons.");

    $line = "INSERT INTO `sources` 
        (`name`, `description`, `link_uri`, `do_not_index`, `auto_import`, `file_path`, `facet_value_id`,  `snippet_language`, `snippet_category` ) 
        VALUES 
        (\"{$name}\",
        \"{$description}\",
        'https://github.com/worldflora/wfo-text-content/tree/main/data/wcvp/geography', 
        0,
        1, 
        '{$remote_path}',
        {$fv['id']},
        null,
        null
        );\n";

    $line = str_replace("\n", ' ', $line);
    $line .= "\n";
    echo $line;
    fputs($out, $line);

}
fclose($out);



// get a list of the files

