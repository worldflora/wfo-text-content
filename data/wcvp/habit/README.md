# Habit data extracted from WCVP

A simple script is used to extract approximations of habit from the name matched WCVP file based on the occurrence of key words in the lifeform_description field.

There is probably a better source of this data but it is a starting place!

The script accepts a keyword on the command line and generates the associated files. Obviously this is not Natural Language Processing. If the description says "not an epiphyte" then it will be scored as an epiphyte because it contains that word (that never occurs). The nature of the data suggests negation cases won't exist. The classes of habit will be broad. "shrub" will include subshrubs because of the embedded word. Some stemming can be used: epiphyt (for epiphytic and epiphyte). 

The zip file names include the number of lines in the file to help with estimating import time.

A sidecar file is created that contains all the lifeform descriptions included for that keyword which allows for a precise description of what the facet includes and to sanity check that nothing totally inappropriate is included.

