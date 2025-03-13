# e-flora South Africa Darwin Core Descriptions from IPT

The file contains tab delimited data on descriptions and vernacular names well matched to wfo ids.

Process:

1. Unzip the file
2. Import each of description, reference, taxon, vernacularname into SQLite database called /working/sa.sqlite. SQLite databases are in .gitignore so won't be checked in. You need to do this locally.
3. Delete the files that came out the DwC zip. No need to check them into github.
4. Run the script ...