> Revised scientific report and device/provenance comparison: manuscript/EEG_scientific_report.pdf and manuscript/manuscript.md.

# EEG results: EO, EC and TCF

**Exploratory single-person analysis.** TCF was recorded with eyes closed and is compared principally with EC. These are recording differences, not proof of a TCF effect.

## Main observations

The broad scalp summary showed lower alpha power during TCF than EC (−9.7%) and higher delta power (+20.8%). Posterior alpha was 11.5% lower and posterior delta 51.9% higher. The magnitude of the low-frequency difference depends on the region and artifact threshold. Alpha reduction was similar across the tested sensitivity analyses.

Both eyes-closed spectra were dominated by low-frequency power and did not show a prominent 8–13 Hz peak. Posterior absolute alpha was actually lower in EC than EO in this pipeline (−44.9%). This does not establish a physiological abnormality; residual artifact, state differences, reference and recording/export details require review.

## Principal comparison: TCF versus EC

| Region | Band | EC power (µV²) | TCF power (µV²) | Change |
|---|---|---:|---:|---:|
| Scalp | Delta | 36.35 | 43.90 | +20.8% |
| Scalp | Theta | 8.23 | 7.81 | -5.1% |
| Scalp | Alpha | 5.09 | 4.60 | -9.7% |
| Scalp | Beta | 9.07 | 9.06 | -0.1% |
| Posterior | Delta | 45.63 | 69.32 | +51.9% |
| Posterior | Theta | 8.99 | 8.60 | -4.4% |
| Posterior | Alpha | 5.25 | 4.65 | -11.5% |
| Posterior | Beta | 9.26 | 8.17 | -11.7% |

Power is the average of channel powers, not the power of a channel-averaged waveform. Scalp and posterior estimates use different acceptance masks. Percentage changes are descriptive, without statistical significance or causal interpretation.

## All conditions: posterior power

| Band | EO (µV²) | EC (µV²) | TCF (µV²) |
|---|---:|---:|---:|
| Delta | 78.10 | 45.63 | 69.32 |
| Theta | 26.43 | 8.99 | 8.60 |
| Alpha | 9.53 | 5.25 | 4.65 |
| Beta | 9.62 | 9.26 | 8.17 |

Posterior relative alpha was 8.47% in EO, 7.78% in EC and 5.11% in TCF. The TCF–EC decrease is 2.67 percentage points; this is not the same quantity as the −11.5% absolute-alpha change. Relative changes partly reflect changes in power in other bands.

## Quality and usable data

| Condition | Recorded | Candidate epochs | Scalp accepted | Posterior accepted |
|---|---:|---:|---:|---:|
| EO | 362 s | 88 | 10 / 88 (40 s; 11.4%) | 55 / 88 (220 s; 62.5%) |
| EC | 377 s | 92 | 49 / 92 (196 s; 53.3%) | 78 / 92 (312 s; 84.8%) |
| TCF | 284 s | 69 | 49 / 69 (196 s; 71.0%) | 60 / 69 (240 s; 87.0%) |

Candidate counts exclude the first and last complete four-second epochs. T8 was essentially flat and F3 showed persistent excessive amplitude; both were excluded consistently. M1 and M2 were omitted from scalp summaries. EO contained substantial frontal contamination, compatible with eye activity but not confirmed without EOG. TCF included conspicuous transients, particularly near its end. Automatic screening does not eliminate every artifact. The very small retained EO scalp sample makes that comparison especially fragile.

## Sensitivity of TCF versus EC

| Analysis | Scalp alpha change | Posterior alpha change | Posterior delta change |
|---|---:|---:|---:|
| Primary, 150 µV | -9.7% | -11.5% | +51.9% |
| Stricter, 100 µV | -11.5% | -12.4% | +29.7% |
| First 280 s per condition | -11.3% | -10.5% | +42.8% |
| Boundary epochs included | -9.7% | -11.8% | +52.9% |

The sign of the alpha difference is stable across these choices, but this does not distinguish a true intervention-associated change from fatigue, order, expectancy or residual contamination. Delta changes vary appreciably with stricter artifact screening. No high-pass or notch filter was applied; interpret low-frequency power conservatively.

## Suggested wording for reporting

> In this exploratory single-participant recording sequence, TCF was associated with lower alpha-band power than the preceding eyes-closed condition, with reductions of approximately 10% across the included scalp electrodes and 11% across posterior electrodes. Delta-band power was higher, although the magnitude varied with region and artifact-rejection threshold. These descriptive findings cannot be attributed specifically to TCF because condition order was fixed, no sham condition or repeated blocks were available, and substantial signal-quality limitations remained.

## What is and is not complete

The EDFs have been analyzed, quality decisions exported, figures inspected, spectral scaling checked with a known-amplitude sinusoid, and header-redacted data copies verified to preserve all original signal bytes. The numerical outputs were produced in Python. Equivalent base-R code is included but has not been run here because an R runtime was unavailable. The repository provides an R-versus-Python comparison check for a local R run.

This is a preliminary research analysis, not an EEG clinical interpretation, an independently validated artifact-cleaning pipeline, or evidence establishing a consciousness field. More defensible inference would require repeated/counterbalanced or randomized EC–TCF/sham blocks, monitoring of vigilance and artifacts, and additional independent participants.

## Files and next steps

Read `METHODS.md` for the full analysis specification and missing acquisition details. Use `README.md` for R/Python commands and GitHub upload instructions. All three header-redacted EDFs are included under `data/anonymized/`; original identifiers and actual recording dates/times are not included. Public release still requires authorization for the participant data. No repository has been published.

Technical references and contextual research are listed in `METHODS.md`.
