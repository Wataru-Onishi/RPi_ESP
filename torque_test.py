import os
from dynamixel_sdk import *  # Uses Dynamixel SDK library

# Control table address
ADDR_OPERATING_MODE = 11                      # Operating mode address
ADDR_TORQUE_ENABLE = 64                       # Torque enable address
ADDR_GOAL_CURRENT = 102                       # Goal current address
ADDR_GOAL_POSITION = 116                      # Goal position address
ADDR_PRESENT_POSITION = 132                   # Address of current position
ADDR_CURRENT_LIMIT = 38                       # Current limit address (Assuming this address for example)

# Data Byte Length
LEN_GOAL_CURRENT = 2
LEN_GOAL_POSITION = 4

# Protocol version
PROTOCOL_VERSION = 2.0                        # See which protocol version is used in the Dynamixel

# Default setting
DXL_ID = 7                                    # Dynamixel ID: 7
BAUDRATE = 57600                              # Dynamixel default baudrate: 57600
DEVICENAME = '/dev/DYNAMIXEL'                 # Check which port is being used on your controller

TORQUE_ENABLE = 1                             # Value for enabling the torque
TORQUE_DISABLE = 0                            # Value for disabling the torque

# Operating Modes
EXTENDED_POSITION_CONTROL_MODE = 4            # Extended position control mode (this might need to be changed based on your motor's model)

# Goal settings
goal_current_mA = 6                           # Goal current in mA (this is the maximum operating current we're aiming for)
current_limit_mA = 6                          # Current limit in mA

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
    packetHandler.write2ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_CURRENT, int(current / 0.1))  # Assuming current needs to be set in 0.1mA units

def set_current_limit(limit):
    packetHandler.write2ByteTxRx(portHandler, DXL_ID, ADDR_CURRENT_LIMIT, int(limit / 0.1))  # Assuming limit needs to be set in 0.1mA units

def set_goal_position(position):
    packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_POSITION, position)

# Ensure Dynamixel has been successfully connected
if enable_torque(TORQUE_ENABLE)[0] != COMM_SUCCESS:
    print("Failed to enable torque!")
    quit()

# Set operating mode and current limit
set_operating_mode(EXTENDED_POSITION_CONTROL_MODE)
set_current_limit(current_limit_mA)  # Set the current limit to 6mA

print("Dynamixel has been successfully connected and current limit is set.")

try:
    while True:
        print(f"Press 1 to set current {goal_current_mA}mA and move to position 1000, or type 'exit' to exit.")
        data = input()
        if data == '1':
            set_goal_position(1000)  # Set the goal position to 1000
            set_goal_current(goal_current_mA)  # Set the goal current to 6mA
            print(f"Setting {goal_current_mA}mA current and moving to position 1000.")
        elif data == 'exit':
            break
        else:
            print("Invalid input. Please try again.")
finally:
    enable_torque(TORQUE_DISABLE)
    portHandler.closePort()
