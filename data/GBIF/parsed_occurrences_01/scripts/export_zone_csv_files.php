<?php

/*

    This will generate the CSV files, one per zone, from the 
    database table that was created in the reverse_geocode_by_zone.php. 

    Run once script - probably done another way with the next data release.

*/

// get the database connection.
require_once('../../../../../wfo_fyllo_secrets.php');
$mysqli = new mysqli($db_host, $db_user, $db_password, $db_database); 

// get a list of the country codes to work through

$response = $mysqli->query("SELECT `zone`, count(*) as n FROM kew_geo.global_zones group by `zone` order by `zone`;");
$zones = $response->fetch_all(MYSQLI_ASSOC);
$response->close();

foreach ($zones as $zone) {
    echo $zone['zone'];
    echo "\t";
    echo number_format($zone['n'], 0);
    echo "\t";


    // get a file for output
    $filename = "../out/zones/{$zone['zone']}.csv";
    $out = fopen($filename, 'w');

    // write a header
    $header = array('wfo_id', 'wcvp_plant_id', 'wcvp_name', 'specimen_count');
    for ($i=1; $i < 11 ; $i++) { 
       $header[] = 'example_specimen_' . $i;
    }
    fputcsv($out,  $header, escape: "\\");

    // work through all the entries for that country
    $response = $mysqli->query("SELECT * FROM kew_geo.global_zones where `zone` = '{$zone['zone']}' order by wcvp_name;");
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
    $zip->addFile($filename,"{$zone['zone']}.csv");
    $zip->close();

    echo "\tunlinking";
    unlink($filename);

    // zip up the file

    echo "\tdone\n";


}
