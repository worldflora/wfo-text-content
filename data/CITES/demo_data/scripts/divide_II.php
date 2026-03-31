<?php


$in = fopen("appendix_II.csv", 'r');

$header = fgetcsv($in);

$file_count = 0;

$out = fopen("appendix_II_{$file_count}.csv", 'w');
fputcsv($out, $header);

$line_count = 0;
while($row = fgetcsv($in) ){
	
	fputcsv($out, $row);
	$line_count++;
	// switch files
	if($line_count > 10000){
		echo "Switch files\n";
		fclose($out);
		$file_count++;
		$out = fopen("appendix_II_{$file_count}.csv", 'w');
		fputcsv($out, $header);
		$line_count = 0;
	}
	
}

fclose($out);
fclose($in);