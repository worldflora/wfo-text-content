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
    if ($line_count < 18680617) continue; // skip to where we left off.

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


    // calculate the zones it belongs to based on lat and lon
    $zones = array();

    // Tropical Band: Plants occuring above -23.4° and below +23.4° latitude.
    if($lat > -23.4 && $lat < 23.4) $zones[] = 'tropical';

    // Northern Temperate Band: Plants occuring above +23.4° and below +60° latitude.
    if($lat >= 23.4 && $lat < 60) $zones[] = 'temperate-northern';

    // Southern Temperate Band: Plants occuring above -60° and below -23.4° latitude.
    if($lat <= -23.4 && $lat > -60) $zones[] = 'temperate-southern';

    // Temperate Bands: Plants occuring in either Northern or Southern temperate zones.
    if(in_array('temperate-northern', $zones) || in_array('temperate-southern', $zones) ) $zones[] = 'temperate';

    // Arctic Band: Plants occuring above +60° latitude.
    if($lat >= 60 ) $zones[] = 'arctic';

    // Antarctic Band: Plants occuring below -60° latitude.
    if($lat <= -60 ) $zones[] = 'antarctic';

    // Polar Bands: Plants occuring in Arctic or Antarctic regions.
    if(in_array('arctic', $zones) || in_array('antarctic', $zones) ) $zones[] = 'polar';

    // Western Segment: The zone from -30° to -170° longitude. 
    if($lon <= -30 && $lon > -170) $zones[] = 'western';

    // Afro-European Segment: From -30° to +60° longitude.
    if($lon > -30 && $lon <= 60) $zones[] = 'afro-european';

    // South Asian Segment: From +60° to +95° longitude.
    if($lon > 60 && $lon <= 95) $zones[] = 'asian-south';

    // East Asian Segment: From +95° to -170° longitude. 
    // note switch to OR as we are going around the back of the world
    if($lon > 95 || $lon <= -170) $zones[] = 'asian-east';

    // report the zones
    echo "{$wcvp_row['wfo_id']}\t";
    $zones_string = implode("\t", $zones);
    echo $zones_string;

    $wcvp_plant_name_safe = $mysqli->real_escape_string(substr($wcvp_row['wcvp_name'], 0, 99));

    // work through the zones and add them to the database table
    foreach ($zones as $zone) {
         $key = "{$wcvp_row['wfo_id']}-{$zone}"; // primary key is combination of two - keep it simple
         $sql = "INSERT INTO kew_geo.global_zones 
            (`key`, `wfo_id`, `zone`, `wcvp_name`, `wcvp_name_id`, `occurrence_count`, `occurrences`)
            VALUES
            ('{$key}', '{$wcvp_row['wfo_id']}', '{$zone}', '{$wcvp_plant_name_safe}', {$wcvp_row['wcvp_plant_id']}, 1, '{$row['Ctrl_gbifID']}' )
            ON DUPLICATE KEY UPDATE occurrence_count=occurrence_count + 1, occurrences = IF( occurrence_count < 11 AND LOCATE('{$row['Ctrl_gbifID']}', occurrences) = 0 , concat_ws(',', occurrences, '{$row['Ctrl_gbifID']}'), occurrences);";
             $mysqli->query($sql);
    }

    echo "\tdone\n";
}
