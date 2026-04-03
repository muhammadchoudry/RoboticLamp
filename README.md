# RoboticLamp

A real-life animatronic recreation of the Pixar Luxo Jr. lamp — capable of expressive movement and dynamic maneuvers like weight-redistribution jumping.

This project spans simulation, mechanical design, electronics, and control systems.

---

## Project Goals

- **Simulate** the lamp's linkage and physics in MuJoCo before committing to hardware
- **Design** a 3D-printable chassis with integrated servo and electronics housing
- **Build** a physical prototype using Dynamixel-class servos
- **Control** the lamp with progressively advanced controllers: position → trajectory → dynamic

---

## Repository Structure

```
RoboticLamp/
├── simulation/
│   ├── models/          # MuJoCo XML scene and robot definitions
│   ├── envs/            # Gym-compatible environment wrappers
│   ├── controllers/     # PID, MPC, and RL-based controllers
│   └── scripts/         # Scripts to run, visualize, and benchmark
├── cad/
│   ├── fusion360/       # Fusion 360 source files (.f3d)
│   └── stl/             # Exported STL files for 3D printing
├── firmware/
│   ├── src/             # Microcontroller source code
│   └── config/          # Servo configs, pin maps, calibration
├── docs/
│   ├── design_notes.md
│   └── images/
├── requirements.txt
└── .gitignore
```

---

## Mechanical Overview

The lamp is based on a **parallelogram linkage**, which keeps the head level as the arm moves. Actuated joints:

| Joint        | Axis  | Notes                           |
|--------------|-------|---------------------------------|
| Base rotation | Yaw  | Spins the whole lamp left/right |
| Lower arm    | Pitch | Lifts/lowers the main arm       |
| Upper arm    | Pitch | Controls elbow angle            |
| Head tilt    | Pitch | Keeps head level (can be passive) |
| Head pan     | Yaw   | Optional, for expressiveness    |

---

## Simulation Stack

- **Physics engine:** [MuJoCo](https://mujoco.org/)
- **Python bindings:** `mujoco` (official DeepMind package)
- **RL (future):** Stable-Baselines3 + Gymnasium

### Getting Started

```bash
git clone https://github.com/muhammadchoudry/RoboticLamp.git
cd RoboticLamp
pip install -r requirements.txt
python simulation/scripts/run_sim.py
```

---

## Roadmap

- [ ] Phase 1 — MuJoCo model of lamp linkage
- [ ] Phase 2 — Position controller (pose the lamp)
- [ ] Phase 3 — Trajectory controller (smooth motion)
- [ ] Phase 4 — Dynamic controller (jumping/hopping)
- [ ] Phase 5 — CAD design with servo/electronics housing
- [ ] Phase 6 — Physical prototype build
- [ ] Phase 7 — Deploy control system to hardware

---

## References

- [Luxo Jr. (1986) — Pixar Short Film](https://www.pixar.com/luxo-jr)
- [MuJoCo Documentation](https://mujoco.readthedocs.io/)
- [Whole-body Momentum Control](https://arxiv.org/abs/1908.00585)

---

## License

MIT
