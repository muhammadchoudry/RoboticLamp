"""Render an offscreen snapshot of the Luxo lamp model to a PNG file.

No display or mjpython needed — uses MuJoCo's offscreen renderer.
"""

import os
import mujoco
import numpy as np

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    model_path = os.path.join(script_dir, "..", "models", "luxo.xml")
    model_path = os.path.normpath(model_path)
    output_path = os.path.join(script_dir, "..", "..", "docs", "images", "luxo_snapshot.png")
    output_path = os.path.normpath(output_path)

    print(f"Loading model from: {model_path}")
    model = mujoco.MjModel.from_xml_path(model_path)
    data = mujoco.MjData(model)

    # Step a few times to let the model settle
    for _ in range(500):
        mujoco.mj_step(model, data)

    # Set up offscreen renderer
    width, height = 800, 600
    renderer = mujoco.Renderer(model, height=height, width=width)

    # Configure camera - front-right view, slightly above
    renderer.update_scene(data)
    camera = mujoco.MjvCamera()
    camera.type = mujoco.mjtCamera.mjCAMERA_FREE
    camera.lookat[:] = [0.0, 0.0, 0.12]  # Look at mid-height of lamp
    camera.distance = 0.5                  # Close enough to see detail
    camera.azimuth = -135                  # Front-right angle
    camera.elevation = -20                 # Slightly above

    renderer.update_scene(data, camera=camera)
    pixels = renderer.render()

    # Save as PNG
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    if HAS_PIL:
        img = Image.fromarray(pixels)
        img.save(output_path)
    else:
        # Fallback: save as raw PPM (no dependencies needed)
        output_path = output_path.replace(".png", ".ppm")
        with open(output_path, "wb") as f:
            f.write(f"P6\n{width} {height}\n255\n".encode())
            f.write(pixels.tobytes())

    print(f"Snapshot saved to: {output_path}")


if __name__ == "__main__":
    main()
