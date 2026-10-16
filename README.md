The final updates, and concluded research and observations can be observed via the following vercel-deployed website : https://photometry.vercel.app/

# ML-Assisted Photometry of Faint Stars

This project explores how accurately the brightness of faint stars can be measured from noisy astronomical images, and whether machine learning offers any advantage over conventional photometric methods.

I generated a dataset of 10,000 synthetic stellar images and implemented four approaches to estimate stellar flux: aperture photometry, Gaussian point-spread-function (PSF) fitting, Ridge regression, and a convolutional neural network (CNN).

The aim was not necessarily to make machine learning outperform traditional methods, but to compare how these approaches behave under the same observational conditions.

## What I Built

- Generated 10,000 synthetic 32 × 32 pixel stellar images with known flux values, background noise, and simulated observational variations.
- Implemented aperture photometry to estimate stellar brightness by summing pixel intensities and subtracting the surrounding background.
- Implemented Gaussian PSF fitting to estimate flux by modelling the distribution of light across a star's image.
- Trained a Ridge regression model as a classical machine-learning baseline.
- Built and trained a CNN to estimate stellar flux directly from image cutouts.
- Evaluated all four methods on the same 2,000 held-out test images.
- Compared predictions using mean absolute error (MAE), root mean squared error (RMSE), and bias.

## Results

| Method | MAE (electrons) | RMSE (electrons) | Bias (electrons) |
|---|---:|---:|---:|
| Aperture photometry | 61.13 | 79.64 | 2.71 |
| Gaussian PSF fitting | **54.63** | **72.44** | 3.78 |
| Ridge regression | 85.90 | 109.60 | 3.65 |
| CNN | 76.06 | 99.25 | 13.35 |

Gaussian PSF fitting achieved the lowest MAE and RMSE in this experiment. The CNN performed better than Ridge regression but did not outperform either classical photometric method.

One of the more interesting findings was that a relatively simple mathematical model of how a star's light spreads across an image was more accurate than the trained ML models under the simulated conditions.

This doesn't mean machine learning is unsuitable for astronomical photometry. It suggests that conventional methods can be difficult to outperform when their assumptions closely match the data.

## What I Learned

- How astronomical images represent stellar flux and how noise affects photometric measurements.
- How aperture photometry and PSF fitting estimate brightness using different assumptions.
- How to build and evaluate regression models for scientific measurements.
- Why comparing machine-learning models against established numerical methods is important.
- How to interpret prediction errors, systematic bias, and negative experimental results.

## Limitations

- The experiments used synthetic astronomical images rather than real telescope observations.
- The results depend on the simulated PSF shapes, noise distributions, and background conditions.
- Performance on real astronomical datasets has not yet been established.
- The reported comparison does not demonstrate that machine learning is generally inferior to PSF fitting.

## Tools Used

- **Python:** Dataset generation and analysis
- **NumPy and SciPy:** Numerical processing and fitting
- **Astropy:** Astronomical image handling
- **scikit-learn:** Ridge regression
- **PyTorch:** CNN implementation and training
- **Matplotlib:** Results visualisation

## Conclusion

This project was an attempt to understand where machine learning fits into a problem that already has well-established scientific solutions.

The main result was that Gaussian PSF fitting remained the most accurate approach on the synthetic test set, despite the use of more flexible data-driven models.

The next step would be to evaluate these methods on real astronomical observations and investigate whether machine learning becomes more useful under more complex imaging conditions.
