<?php

require_once('../../../../scripts/LanguageCodes.php');

// simple script to output the 

echo "\nThis will generate the text snippets.\n";

// open the sqlite db - this should have been populated by you using the sqlite client

$db = new SQLite3('../working/sa.sqlite', SQLITE3_OPEN_READWRITE);

$results = $db->query(
    "SELECT * FROM `description`  as d
JOIN `reference` as r on d.source = r.identifier and d.id = r.id
    ORDER BY
        d.language,
		d.id,
		d.source,
        CASE d.`type`
        WHEN 'Morphology' THEN 1
        WHEN 'Diagnostic' THEN 2
		WHEN 'Habitat' THEN 3
        WHEN 'Distribution' THEN 4
        WHEN 'ChromosomeNr' THEN 5
        END
    "
);

$current_id = null;
$current_cite = null;
$current_language = null;
$description = null;
$out = null;
while ($row = $results->fetchArray()) {
   
    $lang_code = LanguageCodes::getCode($row['language']);

    // if the language has changed we change files
    if($row['language'] != $current_language || !$out){

        if($out) fclose($out);

        $out = fopen('../out/description_' . $lang_code . '.csv', 'w');
        fputcsv($out, array(
            'wfo_id',
            'description',
            'citation',
            'language'
        ));
        $current_language = $row['language'];
    }

    // if we moving to a new output row
    if($row['bibliographicCitation'] != $current_cite || $row['id'] != $current_id){
        
        // if we have a description we write out a line
        if($description){
            fputcsv($out, array(
                $current_id,
                $description,
                $current_cite,
                $current_language
            ));
        }

        $current_cite = $row['bibliographicCitation'];
        $current_id = $row['id'];
        $description = "{$row['type']}: {$row['description']}";
    }else{
        $description .= "\n{$row['type']}: {$row['description']}";
    }


}

if($description){
    fputcsv($out, array(
        $current_id,
        $description,
        $current_cite,
        $current_language

    ));
}

fclose($out);

echo "All done\n";

