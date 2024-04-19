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

# Current control mode and position control mode setting
CURRENT_CONTROL_MODE = 0                       # Current control mode
POSITION_CONTROL_MODE = 3                      # Position control mode (extended position control mode might be 4)

# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    input()
    quit()

# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    input()
    quit()

# Enable Dynamixel Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel has been successfully connected")

while True:
    print("Press 1 to set 6mA current, 2 to move to position 1800, 3 to move to position 0, or type 'exit' to exit.")
    data = input()
    if data == '1':
        # Set to current control mode
        packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_OPERATING_MODE, CURRENT_CONTROL_MODE)
        # Set goal current
        packetHandler.write2ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_CURRENT, 6)
        print("Setting 6mA to Dynamixel")
    elif data == '2':
        # Set to position control mode
        packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_OPERATING_MODE, POSITION_CONTROL_MODE)
        # Move to position 1800
        packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_POSITION, 1800)
        print("Moving to position 1800")
    elif data == '3':
        # Set to position control mode
        packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_OPERATING_MODE, POSITION_CONTROL_MODE)
        # Move to position 0
        packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_POSITION, 0)
        print("Moving to position 0")
    elif data == 'exit':
        break
    else:
        print("Invalid input. Please try again.")

# Disable Dynamixel Torque
packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
# Close port
portHandler.closePort()
