# WFO Text Content 

__At the moment this is a proposal, subject to change.__

This is a repository for managing text contributions and files derived from these contributions.

## Rationale & Workflow

__Many hands make light work:__ If the work of preparing textual data for import to the WFO Portal was shared between centres more people could contribute.

__Too many cooks spoil the broth:__ If we are going to be a team of people working on the same files we need to be super organised or we will make things worse.

__We can extract faceting data from text:__ It is possible to extract more than text snippets from the submitted flora texts. This can be done alongside preparing descriptive text for import.

How it works:

1. We manage the files in this GitHub repository.
2. Editorial centres clone the repository and have rights to commit the files they have worked on back.
3. By convention we work on separate parts of the repository so we avoid merging of files.
4. We write scripts for processing and reporting but admit that raw text is usually dirty and needs manual/bespoke cleaning.
5. Third parties could fork the repository if they wanted to help by, for expample, writing process scripts that we could pull in if they are necessary. They could also use it as a resource for research.


## Directory Structure

If multiple people are going to work on the data files we need to maintain a strict data structure. This also enables processing and reporting scripts to find files and write outputs to the correct places. Having a predictable depth to the tree is particularly important for this.

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