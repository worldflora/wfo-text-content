<?php

/*

    This will generate the CSV files, one per country, from the 
    database table that was created in the reverse_geocode_by_polygon.php. 

    Run once script - probably done another way with the next data release.

*/

// get the database connection.
require_once('../../../../../wfo_fyllo_secrets.php');
$mysqli = new mysqli($db_host, $db_user, $db_password, $db_database); 

// get a list of the country codes to work through

$response = $mysqli->query("SELECT country_code, count(*) as n FROM kew_geo.country_occurrences group by country_code order by country_code;");
$countries = $response->fetch_all(MYSQLI_ASSOC);
$response->close();

foreach ($countries as $country) {
    echo $country['country_code'];
    echo "\t";
    echo number_format($country['n'], 0);
    echo "\t";


    // get a file for output
    $filename = "../out/countries/{$country['country_code']}.csv";
    $out = fopen($filename, 'w');

    // write a header
    $header = array('wfo_id', 'wcvp_plant_id', 'wcvp_name', 'specimen_count');
    for ($i=1; $i < 11 ; $i++) { 
       $header[] = 'example_specimen_' . $i;
    }
    fputcsv($out,  $header, escape: "\\");

    // work through all the entries for that country
    $response = $mysqli->query("SELECT * FROM kew_geo.country_occurrences where country_code = '{$country['country_code']}' order by wcvp_name;");
    while($row = $response->fetch_assoc()){

        $line = array();

        $line[] = $row['wfo_id'];
        $line[] = $row['wcvp_name_id'];
        $line[] = $row['wcvp_name'];
        $line[] = $row['occurrence_count'];

        $occurrence_ids = explode(',', $row['occurrences']);
        for ($i=0; $i < 10 ; $i++) { 
            if(isset($occurrence_ids[$i])){
                $line[] = "https://www.gbif.org/occurrence/{$occurrence_ids[$i]}";
            }else{
                $line[] = ''; // run out of exemplars so blank column
            }
        }

        fputcsv($out, $line, escape: "\\");

    }

    fclose($out);

    echo "\tzipping";

    $zip = new ZipArchive();
    $zip->open($filename . '.zip', ZipArchive::CREATE);
    $zip->addFile($filename,"{$country['country_code']}.csv");
    $zip->close();

    echo "\tunlinking";
    unlink($filename);

    // zip up the file

    echo "\tdone\n";


}
