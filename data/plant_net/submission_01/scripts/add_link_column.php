<?php

// this takes the matched file and moves it around
// and adds a deep link to PlantNet

$in_file_path = '../working/plantnet_match_k-world-flora_detailed-stats-2025-02-25.csv';

$in = fopen($in_file_path, 'r');
$out = fopen('../out/plant_net.csv', 'w');


// put a new header in 
// Old header looks like this -> wfo_id,wfo_full_name,wfo_check,input_name_string
fputcsv($out, array(
    'wfo_id',
    'PlantNet_link',
    'Name_in_PlantNet',
    'Name_in_WFO',
    'Placement_in_WFO'
));

// throw away the old header
fgetcsv($in);

// work through the rest of the csv
while($line = fgetcsv($in)){

    // skip if we don't have a good wfo
    if(!preg_match('/^wfo-[0-9]{10}$/', $line[0])) continue;

    $name_safe = rawurlencode($line[1]);
    fputcsv($out, array(
        $line[0],
        "https://identify.plantnet.org/en/k-world-flora/species/{$name_safe}/data",
        $line[3],
        $line[1],
        $line[2]
    ));
}

fclose($in);
fclose($out);
