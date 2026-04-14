"""PID position controller for the Luxo lamp joints.

Provides independent PID control for each actuated joint, allowing
the lamp to hold and track target joint angles.
"""

import numpy as np


class PIDController:
    """Multi-joint PID controller.

    Each joint gets independent P, I, D gains. The controller reads
    joint position and velocity sensors and outputs motor torques.
    """

    def __init__(self, kp, ki, kd, num_joints=4):
        """Initialize the PID controller.

        Args:
            kp: Proportional gains, shape (num_joints,) or scalar.
            ki: Integral gains, shape (num_joints,) or scalar.
            kd: Derivative gains, shape (num_joints,) or scalar.
            num_joints: Number of actuated joints.
        """
        self.kp = np.broadcast_to(np.asarray(kp, dtype=float), (num_joints,)).copy()
        self.ki = np.broadcast_to(np.asarray(ki, dtype=float), (num_joints,)).copy()
        self.kd = np.broadcast_to(np.asarray(kd, dtype=float), (num_joints,)).copy()
        self.num_joints = num_joints
        self._integral = np.zeros(num_joints)
        self._prev_error = np.zeros(num_joints)
        self._initialized = False

    def reset(self):
        """Reset integrator and derivative state."""
        self._integral[:] = 0.0
        self._prev_error[:] = 0.0
        self._initialized = False

    def compute(self, target_pos, current_pos, current_vel, dt):
        """Compute control torques for all joints.

        Args:
            target_pos: Desired joint positions, shape (num_joints,).
            current_pos: Current joint positions, shape (num_joints,).
            current_vel: Current joint velocities, shape (num_joints,).
            dt: Timestep in seconds.

        Returns:
            Control signal (torques) for each joint, shape (num_joints,).
        """
        error = np.asarray(target_pos) - np.asarray(current_pos)

        # Integrate error
        self._integral += error * dt

        # Derivative: use velocity sensor directly (more stable than finite diff)
        d_term = -np.asarray(current_vel)

        # On first call, skip derivative kick
        if not self._initialized:
            self._initialized = True

        self._prev_error = error.copy()

        torque = self.kp * error + self.ki * self._integral + self.kd * d_term
        return torque


# Default gains tuned for the Luxo lamp model.
# Order: [base_yaw, lower_arm_pitch, upper_arm_pitch, head_tilt]
DEFAULT_KP = np.array([20.0, 50.0, 40.0, 15.0])
DEFAULT_KI = np.array([2.0, 5.0, 4.0, 1.5])
DEFAULT_KD = np.array([5.0, 10.0, 8.0, 3.0])


def make_default_controller():
    """Create a PID controller with default gains for the Luxo lamp."""
    return PIDController(kp=DEFAULT_KP, ki=DEFAULT_KI, kd=DEFAULT_KD)
