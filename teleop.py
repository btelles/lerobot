import sys
import signal
from lerobot.common.robot_devices.motors.configs import DynamixelMotorsBusConfig
from lerobot.common.robot_devices.motors.dynamixel import DynamixelMotorsBus, TorqueMode
from lerobot.common.robot_devices.robots.configs import KochRobotConfig
from lerobot.common.robot_devices.robots.manipulator import ManipulatorRobot
import tqdm

def config_btelles():
    leader_config = DynamixelMotorsBusConfig(
        port="/dev/ttyACM0",
        motors={
            # name: (index, model)
            "shoulder_pan": (1, "xl330-m077"),
            "shoulder_lift": (2, "xl330-m077"),
            "elbow_flex": (3, "xl330-m077"),
            "wrist_flex": (4, "xl330-m077"),
            "wrist_roll": (5, "xl330-m077"),
            "gripper": (6, "xl330-m077"),
        },
    )

    follower_config = DynamixelMotorsBusConfig(
        port="/dev/ttyACM1",
        motors={
            # name: (index, model)
            "shoulder_pan": (1, "xl430-w250"),
            "shoulder_lift": (2, "xl430-w250"),
            "elbow_flex": (3, "xl330-m288"),
            "wrist_flex": (4, "xl330-m288"),
            "wrist_roll": (5, "xl330-m288"),
            "gripper": (6, "xl330-m288"),
        },
    )

    robot_config = KochRobotConfig(
        leader_arms={"main": leader_config},
        follower_arms={"main": follower_config},
        cameras={},  # We don't use any camera for now
    )
    robot = ManipulatorRobot(robot_config)
    robot.connect()

    return (robot, leader_config, follower_config)


def teleop(seconds=3000, frequency=200):
    robot, _, _ = config_btelles()

    def cleanup(signal, frame):
        print("\nCtrl+C detected. Cleaning up and exiting...")
        robot.follower_arms["main"].write("Torque_Enable", TorqueMode.DISABLED.value)

        robot.disconnect()  # Assuming there's a disconnect method in the robot class
        sys.exit(0)

    signal.signal(signal.SIGINT, cleanup)
    
    for _ in tqdm.tqdm(range(seconds * frequency)):
        robot.teleop_step()

if __name__ == "__main__":
    teleop()

