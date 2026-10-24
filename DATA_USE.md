# Data and provenance

The three EDF copies have patient/recording identification fields and actual date/time fields replaced. Signal samples and task annotation bytes are unchanged. The annotation text in these particular files was inspected and contained recording/task labels. The redaction utility is not a general-purpose anonymizer for other EDFs.

The copies contain human-subject physiological recordings. Public sharing requires the data owner's authority and appropriate participant permission. The supplied demographic fields were not treated as verified participant information. This task has not assigned an open-data license, clinical meaning, or ethics approval to the data.

Do not use the replacement EDF dates/times to reconstruct session timing. Condition order is provided in the manuscript. Original file hashes and copy hashes are recorded in `validation/data_integrity.json`.
