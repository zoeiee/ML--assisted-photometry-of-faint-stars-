# Scientific technical report

## Scope and provenance

This package implements and executes a new synthetic investigation. The original local project artifacts were not provided. Historical aggregate numbers are explicitly unverified. No real observations were used.

## Protocol

10,000 32 × 32 cutouts: 7,000 train, 1,000 validation, 2,000 test. Independent split seeds 20261016–18. Flux is log-uniform 100–3000 electrons; sigma is uniform 1.1–1.5 pixels; baseline sky is 20 electrons/pixel and read noise 3 electrons RMS. Unit-sum finite-stamp PSFs use 2 × 2 subpixel quadrature.

Aperture: measured centroid, radius four, sky annulus 9–13, nominal sigma=1.3 correction. PSF: bounded single circular Gaussian fit, free flux/centre/width/background, seven-pixel fitting region. Ridge and residual Ridge: standardised image-derived features, alpha chosen by validation MAE. CNN: two convolutions, 8/16 channels, pooling, dense 32, scaled inputs/targets, Adam and validation selection.

CNN trained for 30 epochs. Best checkpoint: epoch 23. Test PSF optimisation failures: 2/2000.

## Held-out results

|Method|MAE (e−)|RMSE (e−)|Bias (e−)|Median relative error (%)|95% MAE interval|
|---|---:|---:|---:|---:|---|
|Aperture|41.623|52.844|+7.402|5.680|40.312–43.025|
|PSF|44.361|57.936|+3.014|5.659|42.799–45.924|
|CNN|35.839|46.407|-3.508|4.952|34.478–37.046|
|Ridge|34.837|44.733|+1.389|4.661|33.618–36.010|
|Residual|34.840|44.743|+1.376|4.670|33.614–36.012|
|Ablation|38.186|48.590|+0.985|5.072|36.866–39.533|

## Paired comparisons

Intervals are percentile bootstrap estimates from 1,000 resamples. Negative MAE differences favour the model over PSF. They condition on the trained model and exclude seed-to-seed training uncertainty.

- Aperture: MAE difference -2.738 e−; 95% interval -4.546 to -0.842 e−.
- PSF: MAE difference +0.000 e−; 95% interval +0.000 to +0.000 e−.
- CNN: MAE difference -8.522 e−; 95% interval -10.204 to -6.707 e−.
- Ridge: MAE difference -9.524 e−; 95% interval -10.847 to -8.001 e−.
- Residual: MAE difference -9.521 e−; 95% interval -10.852 to -8.004 e−.
- Ablation: MAE difference -6.175 e−; 95% interval -7.767 to -4.410 e−.

## Controlled conditions

Each condition contains 200 observations, with identical images for every estimator. Parameters and raw arrays are saved. The common condition seed couples nuisance draws; changing Poisson means can change subsequent random draws. There are no scenario confidence intervals or corrected significance tests.

|Condition|Method|MAE (e−)|Bias (e−)|
|---|---|---:|---:|
|faint|Aperture|36.082|+10.661|
|faint|PSF|37.357|+9.902|
|faint|CNN|23.967|+3.684|
|faint|Ridge|29.194|+8.371|
|faint|Residual|29.224|+8.748|
|faint|Ablation|34.644|+7.735|
|bright|Aperture|53.405|+3.746|
|bright|PSF|54.644|+0.776|
|bright|CNN|47.521|-0.343|
|bright|Ridge|47.910|-0.374|
|bright|Residual|47.910|-0.398|
|bright|Ablation|49.414|-0.616|
|sky_high|Aperture|71.148|+4.750|
|sky_high|PSF|82.308|+12.802|
|sky_high|CNN|61.047|+8.375|
|sky_high|Ridge|2265.529|+2265.529|
|sky_high|Residual|2258.974|+2258.974|
|sky_high|Ablation|4109.420|+4109.420|
|read_high|Aperture|72.219|+15.855|
|read_high|PSF|83.611|+21.805|
|read_high|CNN|61.107|+20.425|
|read_high|Ridge|59.132|+24.237|
|read_high|Residual|58.319|+21.528|
|read_high|Ablation|63.385|+4.965|
|wide_psf|Aperture|162.736|-159.699|
|wide_psf|PSF|102.314|+7.781|
|wide_psf|CNN|167.166|-166.740|
|wide_psf|Ridge|144.545|-143.460|
|wide_psf|Residual|144.514|-143.393|
|wide_psf|Ablation|167.389|-165.326|
|elliptical|Aperture|43.915|+8.186|
|elliptical|PSF|44.859|-21.702|
|elliptical|CNN|36.211|+10.570|
|elliptical|Ridge|37.444|+14.034|
|elliptical|Residual|37.375|+13.843|
|elliptical|Ablation|40.799|+5.278|
|moffat|Aperture|123.717|-114.440|
|moffat|PSF|181.253|-163.669|
|moffat|CNN|121.867|-119.086|
|moffat|Ridge|152.393|-148.947|
|moffat|Residual|152.517|-149.048|
|moffat|Ablation|124.048|-116.732|
|crowded|Aperture|357.831|+357.082|
|crowded|PSF|446.959|+425.641|
|crowded|CNN|265.043|+264.003|
|crowded|Ridge|381.804|+380.364|
|crowded|Residual|381.234|+379.817|
|crowded|Ablation|352.087|+351.510|
|gradient|Aperture|45.811|+15.175|
|gradient|PSF|70.986|+22.689|
|gradient|CNN|48.267|-36.864|
|gradient|Ridge|39.707|+1.813|
|gradient|Residual|39.647|+1.590|
|gradient|Ablation|39.721|-2.323|
|control|Aperture|41.889|+9.733|
|control|PSF|43.421|+1.457|
|control|CNN|35.662|-2.682|
|control|Ridge|33.016|+1.668|
|control|Residual|33.037|+1.711|
|control|Ablation|36.729|+3.844|

## Interpretation

Ridge has MAE 34.84 electrons, residual Ridge 34.84, CNN 35.84, aperture 41.62, and PSF 44.36. This run does not reproduce the historical PSF-first ranking. Neither comparison invalidates the other without matching data and estimator assumptions.

Grouped ablation changes Ridge MAE from 34.84 to 38.19. This supports the usefulness of the removed group within this fit, not a causal claim for a particular feature. Residual and direct Ridge are closely related linear models because the baseline PSF estimate is itself a feature.

The free PSF width and centroid can absorb noise, especially on faint sources. A fixed aperture and learned prior may trade variance against bias. These are plausible mechanisms, not isolated causal conclusions. Test conditions outside the training distribution reveal sensitivity; rankings on 200 examples should not be overgeneralised.

## Historical comparison

Historical user-reported MAE: aperture 61.13, PSF 54.63, Ridge 85.90, CNN 76.059 electrons. Historical split membership, metric definitions, weights and predictions could not be checked. Full historical values are preserved separately.

## Reproduction and limitations

See README.md for stage commands, REPRODUCIBILITY.md for seeds and units, and SCIENTIFIC_LIMITATIONS.md for simulator and estimator caveats. All scientific plots come from saved outputs. No original data, real observations, multiple training seeds or M4 hardware validation were available. Browser rendering and Vercel-host deployment were not tested.

## Sources

- Photutils aperture documentation: https://photutils.readthedocs.io/en/stable/user_guide/aperture.html
- Kingma & Ba, Adam: https://arxiv.org/abs/1412.6980
- scikit-learn Ridge: https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html
- Original Distill framework: https://github.com/distillpub/template
- Design reference: https://distill.pub/2021/gnn-intro/
