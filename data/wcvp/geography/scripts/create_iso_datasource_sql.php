<?php

/*
    This is a run once script to generated SQL Insert statements to add 
    data sources for the 300+ Level 3 files
*/
// get the database connection.
require_once('../../../../../wfo_fyllo_secrets.php');
$mysqli = new mysqli($db_host, $db_user, $db_password, $db_database); 

$response = $mysqli->query("SELECT `id`, `code`, `name` FROM wfo_facets.facet_values where facet_id = 1");
$facet_values = $response->fetch_all(MYSQLI_ASSOC);
$response->close();


$out = fopen('../working/iso_insert.sql', 'w');
foreach($facet_values as $fv){

    // check the file exists
    $local_files = glob("../out/iso_countries/{$fv['code']}.csv.zip");
    if(count($local_files) != 1) continue;

    // skip the ones we have already done
    if(in_array($fv['code'], array(
        'AF',
        'AL',
    ))) continue;

    $remote_path = 'data/wcvp/geography/out/iso_countries/' . basename($local_files[0]);

    $name = $mysqli->real_escape_string("{$fv['name']} - WCVP - TDWG Level 3 based.");

    $line = "INSERT INTO `sources` 
        (`name`, `description`, `link_uri`, `do_not_index`, `auto_import`, `file_path`, `facet_value_id`,  `snippet_language`, `snippet_category` ) 
        VALUES 
        (\"{$name}\",
        'Some of the TDWG Level 3 codes correspond to ISO countries (e.g. Zimbabwe), others are unambiguously part of ISO countries (e.g. the states of the United States of America). A mapping file was prepared (a copy is in the raw directory) mapping between Level 3 codes and countries that allowed distributions by country to be extracted from WCVP Level 3 data in the World Checklist of Vascular Plants.',
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

