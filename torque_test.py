import os
from dynamixel_sdk import *  # Uses Dynamixel SDK library

# Control table address
ADDR_OPERATING_MODE = 11                       # Operating mode address
ADDR_TORQUE_ENABLE = 64                        # Torque enable address
ADDR_GOAL_CURRENT = 102                        # Goal current address
ADDR_GOAL_POSITION = 116                       # Goal position address
ADDR_PRESENT_POSITION = 132                    # Address of current position
ADDR_CURRENT_LIMIT = 38                        # Current limit address (example, check your model specification)

# Data Byte Length
LEN_GOAL_CURRENT = 2
LEN_GOAL_POSITION = 4

# Protocol version
PROTOCOL_VERSION = 2.0                         # See which protocol version is used in the Dynamixel

# Default setting
DXL_ID = 7                                     # Dynamixel ID : 7
BAUDRATE = 57600                               # Dynamixel default baudrate : 57600
DEVICENAME = '/dev/DYNAMIXEL'                     # Typically /dev/ttyUSB0 for Linux or "COMx" for Windows

TORQUE_ENABLE = 1                              # Value for enabling the torque
TORQUE_DISABLE = 0                             # Value for disabling the torque

# Operating Modes
EXTENDED_POSITION_CONTROL_MODE = 4             # Extended position control mode

# Position and current settings
goal_position_target = 1000                    # Target position for the motor
current_limit_mA = 6                           # Maximum current limit in mA

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
    enable_torque(TORQUE_DISABLE)  # Disable Torque before changing operating mode
    packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_OPERATING_MODE, mode)
    enable_torque(TORQUE_ENABLE)   # Re-enable Torque after changing operating mode

def set_goal_current(current):
    packetHandler.write2ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_CURRENT, current)

def set_current_limit(current):
    packetHandler.write2ByteTxRx(portHandler, DXL_ID, ADDR_CURRENT_LIMIT, current)

def set_goal_position(position):
    packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_POSITION, position)

# Ensure Dynamixel has been successfully connected
if enable_torque(TORQUE_ENABLE)[0] != COMM_SUCCESS:
    print("Failed to enable torque!")
    quit()

# Set current limit
set_current_limit(current_limit_mA)

print("Dynamixel has been successfully connected and current limit is set.")

try:
    while True:
        print(f"Press 1 to move to position {goal_position_target} with current limit {current_limit_mA}mA, or type 'exit' to exit.")
        data = input()
        if data == '1':
            set_operating_mode(EXTENDED_POSITION_CONTROL_MODE)
            set_goal_position(goal_position_target)
            set_goal_current(current_limit_mA)  # Set the goal current to the maximum allowable current
            print(f"Moving to position {goal_position_target} with current limit of {current_limit_mA}mA.")
        elif data == 'exit':
            break
        else:
            print("Invalid input. Please try again.")
finally:
    enable_torque(TORQUE_DISABLE)  # Disable Torque on exit
    portHandler.closePort()  # Close port
