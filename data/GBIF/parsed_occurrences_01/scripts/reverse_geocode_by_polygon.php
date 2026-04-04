<?php

/*
    This will work through the parsed GBIF data and reverse geocode the
    specimen locations to get their country
    It will then add them to a table in mysql, keeping track of the
    number of specimens in each area

    Run once script assumes kew.wcvp database is available.
    
*/

require_once('../../../../../wfo_fyllo_secrets.php');
$mysqli = new mysqli($db_host, $db_user, $db_password, $db_database); 

$in = fopen('zip://../raw/parseGBIF_useable_rechecked_successfully_plus.csv.zip#parseGBIF_useable_rechecked_successfully_plus.csv' , 'r');

$header = fgetcsv($in, escape: "\\");

print_r($header);

$line_count = 0;
while($line = fgetcsv($in, escape: "\\")){
    
    $line_count++;
   // if ($line_count < 18680617) continue; // skip to where we left off.

    echo number_format($line_count, 0);
    echo "\t";

    $row = array_combine($header, $line);

    // skip it if it isn't flagged as useable
    if($row['parseGBIF_dataset_result'] != 'us'){
        echo "Not useable record, skipping \n";
        continue;
    }

    // get the WFO ID from the taxon
    $wcvp_id = $row['parseGBIF_wcvp_plant_name_id'];

    // get the wfo
    $response = $mysqli->query("SELECT wfo_id, plant_name_id as wcvp_plant_id, concat_ws(' ', taxon_name, taxon_authors) as wcvp_name, powo_id from kew.wcvp where plant_name_id = {$wcvp_id};");
    $rows = $response->fetch_all(MYSQLI_ASSOC);
    if(count($rows) < 1 || !$rows[0]['wfo_id'] || !preg_match('/^wfo-[0-9]{10}$/', $rows[0]['wfo_id'])){
        echo "No WFO ID for $wcvp_id, skipping \n";
        continue;
    }
    $wcvp_row = $rows[0];

    $lat = (double)$row['parseGBIF_decimalLatitude'];
    $lon = (double)$row['parseGBIF_decimalLongitude'];

    // fetch the country from the table
    $response = $mysqli->query("SELECT * FROM kew_geo.country_polygons where ST_Within(ST_PointFromText('POINT({$lat} {$lon})', 4326), `polygon`);");
    $rows = $response->fetch_all(MYSQLI_ASSOC);
    if(count($rows) < 1){
        echo "No country code for {$lat} {$lon}, skipping \n";
        continue;
    }
    $country_row = $rows[0];

    echo "{$wcvp_row['wfo_id']}\t{$country_row['code_2']}\t{$country_row['name']}\n";

    $key = "{$wcvp_row['wfo_id']}-{$country_row['code_2']}"; // primary key is combination of two - keep it simple
    $country_name_safe = $mysqli->real_escape_string($country_row['name']);
    $wcvp_plant_name_safe = $mysqli->real_escape_string(substr($wcvp_row['wcvp_name'], 0, 99));
    $sql = "INSERT INTO kew_geo.country_occurrences 
            (`key`, `wfo_id`, `country_code`, `country_name`, `wcvp_name`, `wcvp_name_id`, `occurrence_count`, `occurrences`)
            VALUES
            ('{$key}', '{$wcvp_row['wfo_id']}', '{$country_row['code_2']}', '{$country_name_safe}', '{$wcvp_plant_name_safe}', {$wcvp_row['wcvp_plant_id']}, 1, '{$row['Ctrl_gbifID']}' )
            ON DUPLICATE KEY UPDATE occurrence_count=occurrence_count + 1, occurrences = IF( occurrence_count < 11, concat_ws(',', occurrences, '{$row['Ctrl_gbifID']}'), occurrences);";
    // keeping the first 10 occurrences we come across.
    $mysqli->query($sql);

}
