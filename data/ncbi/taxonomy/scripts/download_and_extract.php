<?php

// this will download and extract from NCBI 
// see ../README.md first

$download_url = 'https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/new_taxdump/new_taxdump.zip';
$out_file_name = 'rankedlineage.csv';
$out_file_path = '../working/' . $out_file_name;


// if the file doesn't exist then download it
if(!file_exists('../raw/new_taxdump.zip')){
    echo "Downloading new_taxdump.zip now.\n";
    file_put_contents("../raw/new_taxdump.zip", fopen($download_url, 'r'));
    echo "Done downloading.\n";
}else{
    echo "Raw file new_taxdump.zip is already present so NOT downloading. \n";
}

// working through 
$in = fopen('zip://../raw/new_taxdump.zip#rankedlineage.dmp', 'r');

if(!$in){
    echo "Failed to open stream from rankedlineage.dmp in the zip file.\n";
    echo "Maybe unzip it and see if it is there?\n";
    exit;
}

echo "Got stream for rankedlineage.dmp\n";

$out = fopen($out_file_path, 'w');

// add a header (fields are in the readme.txt file in the zip)
fputcsv($out, array(
    "tax_id", 
    "tax_name",
    "species",
    "genus",
    "family",
    "order",
    "class",
    "phylum",
    "kingdom",
    "superkingdom"
));

echo "Working through file.\n";
$counter = 0;
while($line = fgetcsv($in, null, '|')){
    
    $line = array_map('trim', $line); // fields are padded
    if($line[8] != 'Viridiplantae') continue;
    if($line[7] == 'Chlorophyta') continue;
    if($line[6] == 'Charophyceae') continue;
    if(str_contains($line[1], ' sp.')) continue; // no unnamed species
    if(str_contains($line[1], ' cf.')) continue; // no similar to
    if(str_contains($line[1], 'unclassified')) continue; // no similar to
    
    fputcsv($out, $line);
    $counter++;
}
echo "Finished generating file. ". number_format($counter, 0) ." relevant lines found.\n";

fclose($out);
fclose($in);


echo "Zipping...\n";
// turn the out file into a zip file so that it is github friendly
$zip = new ZipArchive();
if ($zip->open($out_file_path . '.zip', ZipArchive::CREATE) === TRUE) {
    $zip->addFile($out_file_path, $out_file_name);
    $zip->close();
    echo "Zipped\n";
    unlink($out_file_path);
} else {
    echo 'Failed to Zip';
}
