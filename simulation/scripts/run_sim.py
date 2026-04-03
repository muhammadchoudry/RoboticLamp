"""Basic simulation script for the Luxo lamp MuJoCo model.

Loads the MJCF model and launches the passive viewer so you can
observe the lamp falling under gravity (no controller active).
This validates that the model loads correctly and the linkage
geometry behaves as expected.
"""

import os
import mujoco
import mujoco.viewer


def main():
    # Resolve path to the MJCF model relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(script_dir, "..", "models", "luxo.xml")
    model_path = os.path.normpath(model_path)

    print(f"Loading model from: {model_path}")
    model = mujoco.MjModel.from_xml_path(model_path)
    data = mujoco.MjData(model)

    print("Model loaded successfully!")
    print(f"  Bodies: {model.nbody}")
    print(f"  Joints: {model.njnt}")
    print(f"  Actuators: {model.nu}")
    print(f"  Timestep: {model.opt.timestep}s")
    print()
    print("Launching passive viewer... Close the window to exit.")

    # Launch the passive viewer - it steps the simulation automatically
    mujoco.viewer.launch_passive(model, data)


if __name__ == "__main__":
    main()
