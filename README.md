# WFO Text Content 

This is a repository for managing text contributions and files derived from these contributions.

__At the moment this is a proposal, subject to change.__


## Directory Structure

If multiple people are going to work on the data files we need to maintain a strict data structure. This also enables processing and reporting scripts to find the files and write them to the correct places. Having a predictable depth to the tree is important for this.

- Text files are placed in a hierarchy within the data directory.
- There is an abitrary two layer hierarchy within this the data directory
- The "organisation" level could be a real organisation like Kew Gardens or a project like Flora Thailand.
- The "publication" is an actual data deposit. e.g. the volume of a flora.
- The update of an existing publication does not count as a new publication. If the data is replacing previous data we rely on GitHub versioning to keep track of the old data.
- Each publication has four subdirectories.
```
|
|-- data
|   |-- oganization_01
|   |   |-- scripts <= code used just for this organisation (optional)
|   |   |-- publication_01
|   |   |   |-- raw <= original data as submitted
|   |   |   |-- work <= any intermediate files produced 
|   |   |   |-- out <= files ready for ingest / publication
|   |   |   |-- scripts <= code used just for this publication (optional)
|   |   |-- publication_02
|   |   |   |-- raw
|   |   |   |-- work
|   |   |   |-- out
|   |   |   |-- scripts
|   |-- oganization_02
|   |   |-- scripts
|   |   |-- publication_01
|   |   |   |-- raw
|   |   |   |-- work
|   |   |   |-- out
|-- scripts <= code utilities used across all organisations
```

## Conventions

- File and directory names should always be lower case without spaces (replace with underscore). Except for:
- Any documentation or notes associated with the content of a directory should be written in a README.md file in the directory. This makes it visible directly in GitHub web. If in doubt document it in the README.md file but remember this is publicly visible open data.
- When numbering is required in file and directory names it should always be zero left padded so that when files and directories are sorted alphabetically they also appear in number order. If there will be a few files then 01,02,03 is sufficient. If there may be more than one hundred in the future then 001,002,003 etc.