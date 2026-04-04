<?php

/*
    Import the geojson so that we can use the geospatial engine
    to see if the points are in it or not

    Run once script
*/

// -d memory_limit=10G

// database connection details outside of git repo
require_once('../../../../../wfo_fyllo_secrets.php');

$mysqli = new mysqli($db_host, $db_user, $db_password, $db_database);  

$files = glob('../raw/country_files/*.json');
foreach($files as $file){

    echo $file;
    echo "\t";

    $json = file_get_contents($file);
    $country = json_decode($json);

    $code_2 = $country->properties->tags->{'ISO3166-1:alpha2'};
    $code_3 = $country->properties->tags->{'ISO3166-1:alpha3'};
    $name = $mysqli->real_escape_string($country->properties->tags->{'name:en'});

    if($code_3 == 'FJI') continue;
    if($code_3 == 'ATA') continue;

    // hack for 180s    
    $geo = json_encode($country->geometry);
 
    echo $code_2;
    echo "\t";
    echo $code_3;
    echo "\t";
    echo $name;
    echo "\n";

    $mysqli->query("INSERT INTO kew_geo.country_polygons (`code_2`, `code_3`, `name`, `polygon`) VALUES ('{$code_2}', '{$code_3}','{$name}',ST_GeomFromGeoJSON('{$geo}'))");


}
