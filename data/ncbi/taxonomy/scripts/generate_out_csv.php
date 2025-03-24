<?php

// see ../README.md first

// php -d memory_limit=2G generate_out_csv.php 

// Use a local matcher if you need to
$matching_api = 'http://localhost:2000/matching_rest.php';
//$matching_api = 'https://list.worldfloraonline.org/matching_rest.php';

// ncbi linking url
$ncbi_url = "https://www.ncbi.nlm.nih.gov/Taxonomy/Browser/wwwtax.cgi?id=";

// cite as NCBI:txid2559747


// load the matching cache if it exists
$cache_file_path = '../working/matching_cache.csv';
$matching_cache = read_cache($cache_file_path);

$input_file_path = 'zip://../working/rankedlineage.csv.zip#rankedlineage.csv';
$in = fopen($input_file_path, 'r');

$out_file_name = 'ncbi_taxonomy_matched.csv';
$out_file_path = '../out/' . $out_file_name;
$out = fopen($out_file_path, 'w');

// we are going to add 3 columns to start of the table
// so add them to the header first
$header = fgetcsv($in);
array_unshift($header, 'wfo_id', 'link_url', 'cite_as'); 
fputcsv($out, $header);

echo "Working through ncbi file...\n";

$counter = 0;
$cache_page = 0;
while($line = fgetcsv($in)){

    $counter++;

    $link_url = $ncbi_url . $line[0];
    $cite_as = 'NCBI:txid' . $line[0];

    // if it is in the cache we don't look for it 
    // again
    if( isset($matching_cache[$line[0]]) ){
        array_unshift($line, $matching_cache[$line[0]], $link_url, $cite_as); 
        fputcsv($out, $line);
        continue;
    }

    continue; // run without lookup, just on cache

    // not got it from the cache so we should look it up with the matching API
    echo number_format($counter, 0);
    echo "\t";
    echo $line[1];
    $response = file_get_contents($matching_api . '?' . http_build_query(array('input_string' => $line[1])) );
    $response = json_decode($response);

    // if we have a perfect match we add it 
    if(isset($response->match) && $response->match != null){
        echo "\t{$response->match->wfo_id}";
        
        $matching_cache[$line[0]] = $response->match->wfo_id; // keep track of matches
        $cache_page++;

        array_unshift($line, $response->match->wfo_id, $link_url, $cite_as); 
        fputcsv($out, $line);

    }else{
        echo "\tNO MATCH";
    }

    echo "\n";

    // we save the cache every 1000
    if($cache_page > 1000){
        write_cache($cache_file_path, $matching_cache);
        $matching_cache = read_cache($cache_file_path);
        $cache_page = 0;
    }

}

fclose($out);
fclose($in);

// when we finish the process we write the cache to file
// so we don't lose it
write_cache($cache_file_path, $matching_cache);


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



function read_cache($cache_file_path){
    if(file_exists($cache_file_path)){
        echo "Reading matching cache\n";
        $cache = array();
        $in = fopen($cache_file_path, 'r');
        while($line = fgetcsv($in)){
            $cache[$line[0]] = $line[1];
        }
        fclose($in);
        return $cache;
    }else{
        // blank array for cache
       return array();
    }
}

function write_cache($cache_file_path, $cache){
        echo "Writing matching cache\n";
        $out = fopen($cache_file_path, 'w');
        foreach ($cache as $key => $value) {
            fputcsv($out, array($key, $value));
        }
        fclose($out);
}