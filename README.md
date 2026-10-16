# ML-Assisted Photometry of Faint Stars

Aditi Jha's synthetic photometry research project. Genuine executed results, classical estimators, Ridge, residual learning and a compact CNN; presented using the official open-source Distill framework.

## Start (MacBook Air M4)

Use Python 3.12, venv and pip. No Conda, CUDA, server or paid service is required.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m research.run
python -m pytest -q
python scripts/build_article.py
python scripts/check_site.py
python -m http.server 8000 --directory public
```

Open http://localhost:8000. The archive already includes built `public/` output and executed results; no retraining is needed to view it. CPU is the tested device. Native M4 installation and runtime were not tested in this Linux environment. MPS is not required or enabled. Package versions are pinned to the executed environment; platform-specific binary availability must be checked when installing on macOS.

## Individual commands

Run these in order for a fresh experiment:

```bash
python -m research.run --stage data
python -m research.run --stage classical
python -m research.run --stage train
python -m research.run --stage evaluate
python -m research.run --stage experiments
python -m research.run --stage figures
python scripts/build_article.py
python -m pytest -q
python scripts/check_site.py
```

`train` trains direct Ridge, residual Ridge, the grouped feature ablation, and the CNN. `configs/default.json` controls run sizes and budget. All paths resolve from the repository root. Stages overwrite their own artifacts; copy an old run before rerunning. `scripts/vendor_framework.py` is only needed to refresh vendor assets, not for normal builds. The built website needs no Python.

## Evidence

- `results/metrics/test_predictions.csv`: same-object comparison, ground truth and diagnostics.
- `results/metrics/summary.json`: computed metrics and paired bootstrap intervals.
- `results/metrics/experiments.csv`: ten conditions, six estimators including ablation.
- `results/models/`: actually fitted Ridge pipelines, CNN checkpoint and epoch history.
- `data/`: all generated cutouts, metadata and classical features.
- `results/experiment_manifest.json`: hashes, seeds, units and machine-readable provenance.
- `report/TECHNICAL_REPORT.md` and `report/VERIFICATION.md`: findings and limits.

The uploaded source contained historical aggregate metrics only, not the original code, arrays or checkpoint. Historical numbers remain unverified and are never mixed with the new run. No real telescope observations were used.

## Repository organisation

The scientific implementation is deliberately compact: `research/core.py` (simulation/photometry/metrics), `research/models.py` (CNN), `research/run.py` (stages/training/evaluation), `research/figures.py` (plots). `website/` contains article source and native framework assets; `public/` is the deployable output. `scripts/build_article.py` builds article prose/tables directly from outputs.

## Framework and licensing

The official https://distill.pub/template.v2.js distribution is vendored, including an unmodified copy. Only its KaTeX URLs are localised in the runtime copy. The requested template commit and original example were inspected, but the downloaded distribution is not asserted to be built from that commit. Shared Distill typography and grid are used without redesign. Article-specific GNN diagrams and editorial branding were not copied. This is not an official Distill publication. See `website/vendor/provenance.json`, LICENSE and NOTICE. Newly generated project code is offered under Apache 2.0; third-party assets retain their licenses.

See DEPLOYMENT.md for Vercel instructions and SCIENTIFIC_LIMITATIONS.md before interpreting results.
# ML--assisted-photometry-of-faint-stars-
