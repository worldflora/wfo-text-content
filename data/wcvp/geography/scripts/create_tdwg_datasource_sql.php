<?php

/*
    This is a run once script to generated SQL Insert statements to add 
    data sources for the 300+ Level 3 files
*/
// get the database connection.
require_once('../../../../../wfo_fyllo_secrets.php');
$mysqli = new mysqli($db_host, $db_user, $db_password, $db_database); 

$response = $mysqli->query("SELECT `id`, `code`, `name` FROM wfo_facets.facet_values where facet_id = 5");
$facet_values = $response->fetch_all(MYSQLI_ASSOC);
$response->close();



$out = fopen('../working/level_3_insert.sql', 'w');
foreach($facet_values as $fv){

    // check the file exists
    $local_files = glob("../out/tdwg_level3/{$fv['code']}_*.csv.zip");
    if(count($local_files) != 1) continue;

    $remote_path = 'data/wcvp/geography/out/tdwg_level3/' . basename($local_files[0]);

    //   echo $local_path .= "\n";
  //  if(!file_exists($local_path)) continue;


    $line = "INSERT INTO `sources` 
        (`name`, `description`, `link_uri`, `do_not_index`, `auto_import`, `file_path`, `facet_value_id`,  `snippet_language`, `snippet_category` ) 
        VALUES 
        ('TDWG Level 3: {$fv['code']} - {$fv['name']} from WCVP',
        '',
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

