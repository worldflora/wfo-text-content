<?php

/*

    Extract habit based on keywords passed on commandline

*/

// get the database connection.
require_once('../../../../../wfo_fyllo_secrets.php');
$mysqli = new mysqli($db_host, $db_user, $db_password, $db_database); 

// get the keyword
if(count($argv) != 2){
    echo "\nYou need to pass a keyword. Hint: you can put it in quotes.\n";
    exit;
}

$keyword = $argv[1];
$keyword_sql_safe = $mysqli->real_escape_string($keyword);
$keyword_file_safe = str_replace(' ', '_', mb_ereg_replace("([^\w\s\d\-_~,;\[\]\(\).])", '', $keyword));

// get a list distributions by TDWG regions
$response = $mysqli->query("SELECT 
        wcvp.wfo_id,
        wcvp.lifeform_description,
        wcvp.ipni_id,
        wcvp.powo_id,
        wcvp.family as wcvp_family,
        wcvp.genus as wcvp_genus, 
        wcvp.taxon_name as wcvp_taxon_name
    FROM kew.wcvp as wcvp
    where lifeform_description like '%{$keyword_sql_safe}%'
    AND wcvp.wfo_id REGEXP '^wfo-[0-9]{10}$'");

// get a file to write to
$file_name = "../out/{$keyword_file_safe}.csv";
$out = fopen($file_name, 'w');

// write a header in the file
fputcsv($out, array(
    "wfo_id",
    "lifeform_description",
    "ipni_id",
    "powo_id",
    "wcvp_family",
    "wcvp_genus", 
    "wcvp_taxon_name"
), escape: "\\");

$line_count = 0;
$lf_descriptions = array();
while ($row = $response->fetch_assoc()) {
    // just write the row to the file
    fputcsv($out, $row, escape: "\\");
    $line_count++;
    echo "\n{$line_count}\t{$row['wcvp_taxon_name']}";

    // keep track of the descriptions used
    if(!in_array($row['lifeform_description'], $lf_descriptions)){
        $lf_descriptions[] = $row['lifeform_description'];
    }
    
}

fclose($out);

echo "\n\nzipping";
$zip = new ZipArchive();

$csv_name = basename($file_name);
$zip_name = "{$file_name}_{$line_count}_.zip";

$zip->open($zip_name, ZipArchive::CREATE);
$zip->addFile($file_name, $csv_name);
$zip->close();

echo "\tunlinking";
unlink($file_name);

// dump the lifeform descriptions to a file
file_put_contents(
        $file_name . '_lifeform_descriptions.txt',
        implode("\n", $lf_descriptions) 
    );

echo "\tdone\n";

