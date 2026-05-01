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
            geo.locality,
            SUBSTRING(geo.locationid,6) as tdwg_level3,
            wcvp.geographic_area as wcvp_geo_note,
            wcvp.ipni_id,
            wcvp.powo_id,
            wcvp.family as wcvp_family,
            wcvp.genus as wcvp_genus, 
            wcvp.taxon_name as wcvp_taxon_name
        FROM kew.wcvp_geo as geo
        JOIN kew.wcvp as wcvp on geo.plant_name_id = wcvp.plant_name_id
        where locationid REGEXP '^TDWG:[A-Z]{3}$'
        AND wcvp.wfo_id REGEXP '^wfo-[0-9]{10}$'
        order by locationid;", MYSQLI_USE_RESULT);

$file_name = null;
$current_level_code = null;
$out = null;
$line_count = 0;
while ($row = $response->fetch_assoc()) {


    // are we starting a new code?
    if($current_level_code != $row['tdwg_level3']){

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

        $current_level_code = $row['tdwg_level3'];
        $safe_country_name = mb_ereg_replace("([^\w\s\d\-_~,;\[\]\(\).])", '', $row['locality']);
        $file_name = "../out/tdwg_level3/{$current_level_code}_{$safe_country_name}.csv";
        $out = fopen($file_name, 'w');

        // write a header in the file
        fputcsv($out, array(
            "wfo_id",
            "locality",
            "tdwg_level3",
            "wcvp_geo_note",
            "ipni_id",
            "powo_id",
            "wcvp_family",
            "wcvp_genus", 
            "wcvp_taxon_name"
        ), escape: "\\");

        // report what we've done
        echo "\n{$row['tdwg_level3']}\t{$row['locality']}";
    }

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

