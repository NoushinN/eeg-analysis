# Acquisition documentation and source comparison

Source: supplied noushin.pdf, brainboost BrainAssistant qEEG report, 53 pages.

| Field | Vendor report | Analyzed exports |
|---|---|---|
| Hardware | eego / ANT Compatibility 2021 (NA-246), p. 2 | Hardware unspecified in EDF signal headers |
| Sampling rate | 2048, p. 2 | 256 Hz |
| Montage | M1~M2, p. 2 | Labels end in -CPz |
| Report version | v26.05a | See results/python_versions.json |
| Segments | EO 06:01; EC 00:13; EC 06:16; Intervention 04:43 | EO 362 s; EC 377 s; TCF 284 s |

The vendor report supplies no intervention-versus-EC quantitative comparison. Its alpha-regulation and EMG scores offer qualitative quality context, not validation of the TCF findings. Reference transformations, sampling-rate changes, EC segment selection, artifact handling and spectral normalization remain unresolved. See manuscript for detailed comparisons and page-level citations.

The original vendor PDF and poster are not bundled because this repository uses metadata-redacted research files. Retain the supplied originals privately for source verification. No participant age or sex has been inferred from the vendor report's demographic fields.
