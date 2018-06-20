# Usage for wordlist.py

Flags can be viewed by running `python3 wordlist.py --help`.

Several of the flags for this script are unlikely to be useful and are basically historical.

`--html` produces one or more html pages containing a table containing a row for each word occurence. Several columns are missing, and this option is made mostly obsolete by `--html_general`. This option contrasts with `--csv` which also produces a file listing all word occurences, but includes more complete information. In both cases, the file is created in the directory from which the script is invoked.

`--sort <sortorder>` sorts the data produced by `--html` or `--csv`. <sortorder> specifies the order in which fields should be used to sort the data. 

ex) `--sort ltfe` will sort first by language, then by text, then by file name, then by edition type.

`--old_system` will cause the words to be identified based on information provided by the LXML ElementTree. This was faster, but was difficult to reason about and was replaced by a character-based approach. This may still be useful for checking against the current results. Previously, this was the default and the current system was invoked by `--new_system`



