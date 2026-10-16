# Scientific limitations

- This is new synthetic research, not a reproduction of the original local project. No original dataset, source code, split IDs, trained weights or per-object predictions were supplied.
- No real observations or synthetic-to-real validation. No calibrated instrument throughput, passband, astrometry or external ground truth.
- One training seed and one baseline test split. Bootstrap intervals condition on fitted models.
- Baseline training is isolated circular Gaussian stars, uniform sky and fixed read-noise RMS; held-out stress conditions intentionally change these assumptions.
- The source location is approximately known. No detection completeness, false-positive rate or blind catalog construction is tested.
- Finite-stamp flux is conserved; it is not an infinite-aperture estimate for broad profiles. Pixel integration is approximate 2 × 2 quadrature.
- Apertures use pixel-centre inclusion and a nominal sigma=1.3 correction; no width-dependent calibrated aperture correction or contamination mask.
- Aperture uncertainty omits centroid, profile and calibration uncertainty. The sky-median variance uses a Gaussian approximation.
- PSF fitting is circular, unweighted apart from a constant local scale, and single-source; it is not a full Poisson likelihood or deblender. Failures are flagged; boundary hits are not separately flagged.
- Direct and residual Ridge share closely related linear function classes; their comparison mainly probes regularisation.
- Feature ablation removes one group, not individual feature attribution. No comprehensive hyperparameter search or multiple-seed CNN experiment.
- Scenario ranking has no multiple-comparison correction or scenario-specific confidence intervals. Shared random seed does not guarantee paired noise across different Poisson means.
- No cosmic rays, saturation, bad pixels, dark-current calibration, correlated noise, detector nonlinearity or atmospheric variability.
- Simulator size is configurable, but the provided estimators and CNN are fixed at 32 × 32.
- CPU execution was tested on Linux, not native Apple Silicon. Browser visual, mobile and interaction QA was unavailable. The official Distill framework is used, but an exact visual match to the GNN article is not claimed.
