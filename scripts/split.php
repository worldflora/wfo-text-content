<?php

$in = fopen("Index_of_CITES_Species_2025-01-29_Plantae_matched.csv", 'r');

$out1 = fopen('appendix_I.csv', 'w');
$out2 = fopen('appendix_II.csv', 'w');
$out3 = fopen('appendix_III.csv', 'w');
$out_other = fopen('appendix_other.csv', 'w');
$out_nc = fopen('appendix_NC.csv', 'w');

$header = fgetcsv($in);

fputcsv($out1, $header);
fputcsv($out2, $header);
fputcsv($out3, $header);
fputcsv($out_other, $header);
fputcsv($out_nc, $header);

while($row = fgetcsv($in) ){
	
		switch($row[13]){
			case'I':
				fputcsv($out1, $row);
				break;
			case'II':
				fputcsv($out2, $row);
				break;
			case'III':
				fputcsv($out3, $row);
				break;
			case'I/II':
				fputcsv($out2, $row);
				break;
			case'I/NC':
				fputcsv($out1, $row);
				fputcsv($out_nc, $row);
				break;
			case'II/NC':
				fputcsv($out2, $row);
				fputcsv($out_nc, $row);
				break;
			case'III/NC':
				fputcsv($out3, $row);
				fputcsv($out_nc, $row);
				break;
			case'NC':
				fputcsv($out_nc, $row);
				break;
			default:
				fputcsv($out_other, $row);
				break;
		}
	
	
}

fclose($in);
fclose($out1);
fclose($out2);
fclose($out3);
fclose($out_other);
fclose($out_nc);