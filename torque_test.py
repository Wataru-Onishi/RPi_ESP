import os
from dynamixel_sdk import *                    # Uses Dynamixel SDK library

# Control table address
ADDR_OPERATING_MODE = 11                       # Operating mode address
ADDR_TORQUE_ENABLE = 64                        # Torque enable address
ADDR_GOAL_CURRENT = 102                        # Goal current address
ADDR_GOAL_POSITION = 116                       # Goal position address
ADDR_PRESENT_POSITION = 132                    # Address of current position

# Data Byte Length
LEN_GOAL_CURRENT = 2
LEN_GOAL_POSITION = 4

# Protocol version
PROTOCOL_VERSION = 2.0                         # See which protocol version is used in the Dynamixel

# Default setting
DXL_ID = 7                                     # Dynamixel ID : 7
BAUDRATE = 57600                               # Dynamixel default baudrate : 57600
DEVICENAME = '/dev/DYNAMIXEL'                  # Check which port is being used on your controller

TORQUE_ENABLE = 1                              # Value for enabling the torque
TORQUE_DISABLE = 0                             # Value for disabling the torque

# Operating Modes
CURRENT_CONTROL_MODE = 0                       # Current control mode
POSITION_CONTROL_MODE = 3                      # Position control mode
EXTENDED_POSITION_CONTROL_MODE = 4             # Extended position control mode (Position + Current)

# Goal settings
goal_current_mA = 6                            # Goal current in mA (baseline current)
spring_target_position = 1000                  # Target position for spring-like behavior
stiffness = 0.1                                # Stiffness factor (mA per encoder unit deviation)

# Initialize PortHandler instance
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Open port
if not portHandler.openPort():
    print("Failed to open the port!")
    quit()

# Set port baudrate
if not portHandler.setBaudRate(BAUDRATE):
    print("Failed to change the baudrate!")
    quit()

def enable_torque(enable):
    return packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, enable)

def set_operating_mode(mode):
    # Disable Torque before changing operating mode
    enable_torque(TORQUE_DISABLE)
    # Write new operating mode to motor
    packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_OPERATING_MODE, mode)
    # Re-enable Torque after changing operating mode
    enable_torque(TORQUE_ENABLE)

def set_goal_current(current):
    packetHandler.write2ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_CURRENT, current)

def set_goal_position(position):
    packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_POSITION, position)

def get_current_position():
    return packetHandler.read4ByteTxRx(portHandler, DXL_ID, ADDR_PRESENT_POSITION)[1]

# Ensure Dynamixel has been successfully connected
if enable_torque(TORQUE_ENABLE)[0] != COMM_SUCCESS:
    print("Failed to enable torque!")
    quit()

print("Dynamixel has been successfully connected")

try:
    set_operating_mode(EXTENDED_POSITION_CONTROL_MODE)
    set_goal_position(spring_target_position)  # Set the target position to aim for
    print(f"Target position set to {spring_target_position}.")

    while True:
        current_position = get_current_position()
        position_error = spring_target_position - current_position
        current_to_apply = goal_current_mA + int(stiffness * position_error)
        set_goal_current(abs(current_to_apply))
        print(f"Adjusted current to {current_to_apply}mA to maintain position at {spring_target_position}.")
        if input("Press 'q' to quit or any other key to continue: ") == 'q':
            break

finally:
    # Disable Torque on exit
    enable_torque(TORQUE_DISABLE)
    # Close port
    portHandler.closePort()
