# Verification report

## Executed

- Generated 10,000 baseline images (7000/1000/2000 train/validation/test).
- Measured all baseline objects with aperture and Gaussian PSF estimators.
- Trained and saved direct Ridge, residual Ridge, grouped-ablation Ridge and CNN models.
- CNN ran 30 epochs, with validation-selected checkpoint and recorded training history.
- Evaluated identical 2,000 held-out objects; saved all predictions and metrics.
- Computed 1,000-replicate bootstrap MAE intervals and paired differences against PSF fitting.
- Ran ten controlled conditions with 200 objects each, saving image arrays, measured features, metadata, predictions and aggregate metrics.
- Generated six research figures, technical report and genuine Distill article.
- Scientific tests: 14 passed, zero skipped in the final run. Exact output: results/science_tests.log.
- Local site checks: all referenced local assets and anchors exist, required native Distill elements are present, the framework differs from its official copy only in local KaTeX URLs, math font paths exist, and Vercel JSON parses.
- JavaScript syntax check: `node --check website/demonstrations.js` passed.

## Not verified or not performed

- Historical metrics, original split membership and original checkpoint: no source artifacts supplied.
- Real astronomical data and synthetic-to-real transfer: not performed.
- Multiple-seed training uncertainty and comprehensive tuning: not performed.
- Native MacBook Air M4 execution and MPS acceleration: not tested; execution was CPU on Linux/Python 3.12.
- Browser layout, exact GNN visual comparison, mobile screenshots, console errors, rendered mathematics/citation/footnote behaviour and interaction events: no permitted browser QA capability was available. Source checks do not establish rendering success.
- Vercel-host deployment: not executed. Static deployment configuration and instructions are included; the private hosted URL delivered separately uses ChatGPT Sites.

## Scope gaps relative to the master brief

The research article is complete as a bounded synthetic study, not a telescope-validated publication. Its main six research figures are static. An optional appendix provides detector/noise/aperture controls, a row selector for a saved PSF fit, a real-data metric explanation and full-comparison metric selection. Browser interaction QA remains unverified. The simulator supports configurable image size, but the delivered estimator/CNN workflow is fixed at 32 × 32. The official Distill distribution is genuine; it is not asserted to be the exact compiled artifact of the requested commit. Shared framework styles are preserved, but GNN-specific components were not copied and exact visual equivalence is unverified. No GitHub repository was published.

Scientific limitations are detailed in SCIENTIFIC_LIMITATIONS.md. Hosting success is confirmed separately by the deployment service before the final URL is delivered.
