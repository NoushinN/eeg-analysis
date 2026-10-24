# EO, EC and TCF: exploratory EEG analysis

**One participant, one session, fixed order EO → EC → TCF. This is a descriptive research analysis, not evidence of a causal TCF effect.**

## Start here

- [Scientific manuscript (PDF)](manuscript/EEG_scientific_report.pdf)
- [Editable manuscript (Markdown)](manuscript/manuscript.md)
- [Device and source comparison](docs/device_and_source_notes.md)
- [Numerical results summary](RESULTS.md)
- [Full processing methods](METHODS.md)

The manuscript contains an abstract, acquisition/device information, methods, results, interpretation, conclusion, source notes and quality figures. The supplied vendor PDF is partly consistent with our quality concerns but provides no intervention-versus-EC comparison. It lists **2048 sampling rate and M1~M2 montage**, whereas the analyzed EDF exports contain **256 Hz signals labelled -CPz**. Those unresolved differences are explicitly documented.

## Main findings

TCF versus EC showed approximately 9.7% lower scalp alpha and 11.5% lower posterior alpha, with higher delta power. The order was fixed and signal quality was limited. No p-values, diagnostic conclusions, benefit/harm claims or TCF-specific causal inference are supported.

## Run in R

No contributed R packages or Python are required for the R analysis. From this repository's root folder:

```sh
Rscript R/analyze.R data/anonymized results_R
Rscript validation/validate_R.R results_R
```

**Execution status:** R code is supplied but has not been executed in the delivery environment. The completed results were generated in Python. The validation script compares an R run against the executed Python reference. Do not describe the delivered results as R-generated until this succeeds.

## Reproduce delivered calculations with Python

Python 3.12 was used; precise versions are in `results/python_versions.json` and `requirements.txt`.

```sh
python -m pip install -r requirements.txt
python validation/analyze_python.py data/anonymized results_python
python validation/check_pipeline.py
```

On Windows, `py` may be used in place of `python`. Run commands from the extracted project folder, not from inside the ZIP viewer. Paths and capitalization should remain unchanged.

## Edit and rebuild the manuscript

`manuscript/manuscript.md` can be edited directly in any text editor and displayed on GitHub. The PDF-generation source is `scripts/render_manuscript.py`; it contains the formatted manuscript text and pulls tables from the numerical results.

```sh
python -m pip install -r requirements-report.txt
python scripts/render_manuscript.py
```

This regenerates both PDF and Markdown from the renderer's text and current result tables. To preserve direct Markdown edits, do not rerun the renderer without transferring those edits into its source. Review PNGs are written to ignored `build/pdf-review/`.

## Repository contents

| Folder/file | Contents |
|---|---|
| `R/` | Base-R analysis and header-redaction code |
| `validation/` | Executed Python analysis, checks and reference data |
| `data/anonymized/` | Three header-redacted EDF copies; signal bytes unchanged |
| `results/` | CSV tables, figures and runtime versions |
| `manuscript/` | Revised scientific PDF and editable Markdown |
| `docs/` | Device metadata and vendor-report comparison notes |
| `scripts/` | Reproducible manuscript renderer and file-integrity verifier |
| `requirements*.txt` | Analysis and report dependencies |
| `MANIFEST.sha256` | Checksums for the packaged project files |

The original unredacted EDFs, original vendor PDF and poster are not included. Keep them privately as source material. Reproduction of the EEG analysis uses the included header-redacted EDF copies.

## Extract and upload to GitHub

1. Download `EEG_GitHub_Repository_v2.zip` and fully extract it. A standard unencrypted ZIP is supplied; `EEG_GitHub_Repository_v2.tar.gz` contains the same folder as an alternative.
2. Open the extracted `eeg-tcf-repository` folder. You should see this README plus the `R`, `results`, `manuscript`, `data` and other folders.
3. Create an empty repository on GitHub. For a browser upload, choose **Add file → Upload files** and upload the contents of the extracted project folder, preserving subfolders. **Do not upload the ZIP itself as the repository content.**
4. Alternatively, use Git from inside the extracted project folder:

```sh
git init
git add .
git commit -m "Add exploratory EEG analysis and manuscript"
git branch -M main
git remote add origin YOUR_REPOSITORY_URL
git push -u origin main
```

No GitHub repository has been created or published by this task. Use a private repository unless public sharing of the human-subject recordings is authorized. Header redaction alone does not guarantee anonymity. No license for redistribution of the data has been assumed; see `DATA_USE.md`.

## Verify extraction

```sh
python scripts/verify_files.py
```

This checks all packaged file hashes against `MANIFEST.sha256`. If you edit a file, a mismatch is expected; the manifest describes the delivered version. Both archives were tested for extraction, and extracted bytes were compared to the original package before delivery.
