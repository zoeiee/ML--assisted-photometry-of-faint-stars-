# Reproducibility

The main configuration is `configs/default.json`. Baseline seeds are 20261016/17/18 for train/validation/test. Scenario seed 20261026 is separate from the baseline streams and common across scenarios; these condition sets are not ten statistically independent surveys. Each has 200 objects. All methods share each observation within a condition.

`python -m research.run` regenerates images, measurements, training, evaluation, controlled conditions and figures. Expected runtime depends on CPU; fitting 12,000 noisy images dominates. New runs overwrite generated artifacts. Python 3.12 and exact package versions are specified in requirements.txt. CPU, two Torch threads and deterministic algorithms were used. Cross-platform floating-point or library differences can change trained weights and last-place digits; bitwise equality on M4 is not promised.

Dataset metadata stores injected source flux, sky, width, centre, ellipticity, orientation, read noise, PSF family, contaminant flux ratio, gradient, object ID and diagnostic SNR. All source fields are independently drawn within each baseline split. The model sees only image-derived inputs. The test split is never used for fitting, preprocessing, early stopping or alpha selection.

Pixel profiles use 2 × 2 midpoint quadrature and finite-stamp normalisation. Gaussian sigma is in pixels. Moffat beta=3 is chosen to match the Gaussian major-axis FWHM parameter. For an elliptical PSF, the axis ratio rescales its minor axis. The simulator supports `generate(...,image_size=40)`; the supplied photometry/CNN pipeline is intentionally fixed to 32 × 32. Arbitrary image-size training would require adapting those estimators.

The saved `.npz` files are NumPy arrays, not FITS telescope data. The Astropy unit test checks the electron convention, and the Photutils test cross-checks centre-inclusion aperture integration. The production aperture routine is a transparent NumPy implementation. `results/models/*.joblib` files should only be loaded from trusted sources; CNN loading uses weights_only=True.

Bootstrap intervals use 1,000 resampled test indices and fixed seed 20261016. They do not incorporate retraining variance. Historical metrics are preserved in `results/historical_reported.json` and cannot be independently recalculated without original artifacts.

The actual figure source is `research/figures.py`; plots derive from saved arrays/CSVs. HTML tables derive from those same results. Educational controls are explicitly separate and do not generate research metrics.
