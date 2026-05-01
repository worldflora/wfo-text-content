<?php

/*

    This pulls the TDWG Level 3 regions out of the WCVP data set
    and into CSV files for import

*/

// get the database connection.
require_once('../../../../../wfo_fyllo_secrets.php');
$mysqli = new mysqli($db_host, $db_user, $db_password, $db_database); 

// get a list distributions by TDWG regions
$response = $mysqli->query("SELECT 
        wcvp.wfo_id,
        iso.iso_code,
        group_concat(SUBSTRING(geo.locationid,6) SEPARATOR ', ') as tdwg_level3,
        wcvp.ipni_id,
        wcvp.powo_id,
        wcvp.family as wcvp_family,
        wcvp.genus as wcvp_genus, 
        wcvp.taxon_name as wcvp_taxon_name
    FROM kew.wcvp_geo as geo
    JOIN kew.wcvp as wcvp on geo.plant_name_id = wcvp.plant_name_id
    JOIN kew_geo.level3_to_iso_map as iso on SUBSTRING(geo.locationid,6) = iso.tdwg_code
    where locationid REGEXP '^TDWG:[A-Z]{3}$'
    AND wcvp.wfo_id REGEXP '^wfo-[0-9]{10}$'
    group by wcvp.wfo_id,
        iso.iso_code,
        wcvp.ipni_id,
        wcvp.powo_id,
        wcvp.family,
        wcvp.genus, 
        wcvp.taxon_name
    order by iso.iso_code;", MYSQLI_USE_RESULT);

$file_name = null;
$current_iso = null;
$out = null;
$line_count = 0;
while ($row = $response->fetch_assoc()) {

    // are we starting a new code?
    if($current_iso != $row['iso_code']){

        // close the existing file if there is one
        if($out){

            echo "\t$line_count";

            fclose($out);
            echo "\tzipping";
            $zip = new ZipArchive();
            $zip->open($file_name . '.zip', ZipArchive::CREATE);
            $zip->addFile($file_name, basename($file_name));
            $zip->close();

            echo "\tunlinking";
            unlink($file_name);

            $line_count = 0;
        } 

        $current_iso = $row['iso_code'];
        $file_name = "../out/iso_countries/{$current_iso}.csv";
        $out = fopen($file_name, 'w');

        // write a header in the file
        fputcsv($out, array(
            "wfo_id",
            "iso_country",
            "tdwg_level3",
            "ipni_id",
            "powo_id",
            "wcvp_family",
            "wcvp_genus", 
            "wcvp_taxon_name"
        ), escape: "\\");

        // report what we've done
        echo "\n{$current_iso}\t";
    }

    // we write a row out if 

    // just write the row to the 
    fputcsv($out, $row, escape: "\\");
    
    $line_count++;
    
}

// close the last file
echo "\t$line_count";

fclose($out);
echo "\tzipping";
$zip = new ZipArchive();
$zip->open($file_name . '.zip', ZipArchive::CREATE);
$zip->addFile($file_name, basename($file_name));
$zip->close();

echo "\tunlinking";
unlink($file_name);


echo "\ndone\n";

