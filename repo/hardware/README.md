# Hardware

**Status: not yet built.** This documents the planned rig so the data schema
in `data/` and the protocol in `paper/tvc_v2.tex` (Section 4) have a concrete
referent. Update this file as parts arrive and design decisions get made or
revised — treat it as a build log, not just a shopping list.

## Bill of materials

Full priced BOM (targeting a $1,000 micro-grant budget) is not duplicated
here to avoid drift between two copies of the same numbers — see the grant
application in this repo's release notes / project history, or regenerate
from `hardware/bom.csv` (below) once it exists.

Planned subsystems:

- **Actuation & sensing** — 2× Feetech STS3215 bus servos (+1 spare), AS5048A
  14-bit magnetic encoders on both joints (independent of commanded angle),
  Teensy 4.1 for a deterministic control loop with logged timing.
- **Thrust & reaction loading** — contra-rotating 2212 brushless pair (so
  net propeller gyroscopic momentum is near zero and can be tested both
  ways per Section 3.6 of the paper), 6 machined inertia discs per axis
  spanning a 4x range of reflected inertia, a reaction torque cell.
- **Instrumentation** — 6-axis IMU (for the Section 5 IMU-vs-encoder
  comparison, not as ground truth), bench DC supply to remove battery sag
  as a confound during identification.
- **Structure & safety** — printed gimbal + reaction fixture, propeller
  guard, e-stop.

## TODO before build starts

- [ ] `hardware/bom.csv` — one row per part, with supplier link, unit cost,
      quantity, and a `status` column (`ordered` / `received` / `installed`)
- [ ] `hardware/cad/` — gimbal and reaction-fixture design files
- [ ] `hardware/wiring.md` — pinout and wiring diagram once the loom is fixed
- [ ] `hardware/firmware/` — Teensy control loop source (separate from
      `analysis/`, which is host-side only)
- [ ] Photos of the assembled rig, once it exists, in `hardware/photos/`

## Safety

Spinning propellers and a reaction-loaded gear train under test are the two
hazards. A polycarbonate guard and hard e-stop are non-negotiable line items
in the budget, not optional. No detailed operating procedure is written yet
because the rig doesn't exist; one will be added here before first power-on,
and referenced from `paper/tvc_v2.tex`.
