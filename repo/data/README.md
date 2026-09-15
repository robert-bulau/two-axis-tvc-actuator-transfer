# Data

**Status: empty.** No hardware has been built and no measurements have been
taken as of this commit. This directory defines the schema that measured
data will follow once the rig described in `hardware/` exists, so that the
analysis code in `analysis/` can be written and tested against synthetic
data now and pointed at real data later without changing its interface.

## Planned layout

```
data/
  raw/
    servo_id/
      axis{1,2}_load{00..05}_chirp_{trial}.csv
      axis{1,2}_load{00..05}_step_{trial}.csv
    boundary_scan/
      config{A,B,...}_gx{value}_run{trial}.csv
  calibration/
    inertia_discs.csv        # measured (not nominal) moment of inertia per disc
    torque_cell_cal.csv
    encoder_cal.csv
  processed/
    servo_bandwidth_by_load.csv
    boundary_predictions_vs_measured.csv
```

## `servo_bandwidth_by_load.csv` (planned columns)

| column | meaning |
|---|---|
| `axis` | 1 or 2 |
| `load_id` | which inertia disc, references `calibration/inertia_discs.csv` |
| `J_refl_kg_m2` | measured reflected inertia for this load |
| `omega_a_hz` | identified first-order bandwidth |
| `omega_a_ci_lo`, `omega_a_ci_hi` | bootstrap confidence interval |
| `model` | which candidate model was fit: `first_order`, `first_order_delay`, `second_order` |
| `fit_residual_rms` | held-out calibration residual |

## `boundary_predictions_vs_measured.csv` (planned columns)

| column | meaning |
|---|---|
| `config_id` | held-out hardware configuration |
| `scan_gain` | which gain was swept (`k_x` or `k_q`) and its value |
| `abscissa_measured` | fitted from free response (log-envelope / Prony) |
| `abscissa_ci_lo`, `abscissa_ci_hi` | bootstrap CI |
| `abscissa_predicted_unloaded` | prediction from the unloaded-calibration model |
| `abscissa_predicted_corrected` | prediction from Eq. (law) with fitted `J_c` |

Every raw file will carry a header with timestamp, firmware/commit hash, and
operator initials. Once real data lands, this README's "Status" line is the
first thing to update, and a `CHANGELOG.md` entry should note which
commit added which batch.
