# Load-Dependent Actuator Bandwidth Limits Calibration Transfer in Two-Axis TVC Rocket Analogues

**Status: analytical results complete and verified; hardware not yet built; no measured data.**

Most small electric thrust-vector-control (TVC) rocket analogues are
controlled using a servo model identified on an unloaded bench, then applied
to a gimbal that carries a motor, propeller, and bracket. This project asks
how much that shortcut costs: does an unloaded first-order servo model
predict the closed-loop stability boundary of a *reaction-loaded*, two-axis
gimbal, and if not, does a one-parameter reflected-inertia correction fix
it?

The full derivation, prior-art audit, and proposed protocol are in
[`paper/tvc_v2.tex`](paper/tvc_v2.tex) ([compiled PDF](paper/tvc_v2.pdf) if
present — see Building below).

## What's here

| path | what it is |
|---|---|
| `paper/` | manuscript source (LaTeX) and figures |
| `analysis/tvc_stability.py` | the analytical core — system matrix, characteristic polynomial, all three propositions — independent of any measured data |
| `analysis/tests/` | regression tests: every number reported in the paper is pinned here |
| `analysis/make_figures.py` | regenerates every synthetic figure in the paper directly from `tvc_stability.py` |
| `data/` | schema for measured data (currently empty — see `data/README.md`) |
| `hardware/` | BOM and build log for the physical rig (not yet built — see `hardware/README.md`) |

## Reproducing the analytical results

```bash
git clone https://github.com/robert-bulau/two-axis-tvc-actuator-transfer.git
cd two-axis-tvc-actuator-transfer
pip install -r requirements.txt
python -m pytest analysis/tests/ -v      # 14 checks, all derivations in the paper
python analysis/make_figures.py          # regenerates paper/figures/*.png
```

Everything under `analysis/` is synthetic/symbolic verification of the
derivations in Section 3 of the paper. It does not depend on, and is not
evidence for, the hardware experiment proposed in Section 4 — that part
hasn't happened yet.

## Building the paper

```bash
cd paper
pdflatex tvc_v2.tex && pdflatex tvc_v2.tex   # run twice for references/TOC
```

Requires a standard LaTeX install (`pdflatex`, `amsmath`, `booktabs`,
`hyperref`, `longtable` — all in `texlive-latex-extra` on Debian/Ubuntu).

## Project status / roadmap

- [x] Corrected rigid-body derivation and PD-cascade stability analysis
- [x] Prior-art audit and novelty scoping
- [x] Symbolic + numerical verification of every derived result
- [ ] Hardware build (funding-dependent — see `hardware/README.md`)
- [ ] Servo identification under load
- [ ] Held-out boundary prediction experiment
- [ ] Public dataset release (Zenodo, with DOI, once data exists)

## Citing this work

See [`CITATION.cff`](CITATION.cff). This is a working preprint, not a
peer-reviewed publication — please cite accordingly.

## License

Code (`analysis/`): MIT, see [`LICENSE`](LICENSE).
Manuscript text and figures (`paper/`): all rights reserved until a
preprint license is chosen for the arXiv submission; the derivations
are freely reusable in spirit but please ask before reproducing figures
verbatim elsewhere.

## Author

Robert Bulau, Colegiul Național "Mihai Viteazul", Ploiești, Romania.
robertbulau8@gmail.com
