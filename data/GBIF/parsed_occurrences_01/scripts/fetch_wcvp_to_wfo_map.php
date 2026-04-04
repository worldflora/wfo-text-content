<?php

/*
    Collect the mapping from the WCVP file we have in the
    database
    This is a run once script so that the mappings are available
    for further use when the db has gone away.
*/

// database connection details outside of git repo
require_once('../../../../../wfo_fyllo_secrets.php');

$mysqli = new mysqli($db_host, $db_user, $db_password, $db_database);  

$out = fopen('../raw/wcvp_to_wfo_map.csv', 'w');

fputcsv($out, array('wfo_id', 'wcvp_plant_id', 'wcvp_name', 'powo_id' ), escape: "\\");

$response = $mysqli->query("SELECT wfo_id, plant_name_id as wcvp_plant_id, concat_ws(' ', taxon_name, taxon_authors) as wcvp_name, powo_id from kew.wcvp where wfo_id not like 'SKIPPED';");

while($row = $response->fetch_assoc()){
    fputcsv($out, array_values($row), escape: "\\");
}

fclose($out);

