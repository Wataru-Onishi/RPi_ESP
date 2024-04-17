import os
from dynamixel_sdk import *                    # Uses Dynamixel SDK library

# Control table address
ADDR_PRO_CURRENT_LIMIT   = 38                  # EEPROM area
ADDR_PRO_GOAL_CURRENT    = 102                 # RAM area
ADDR_PRO_OPERATING_MODE  = 11                  # EEPROM area
ADDR_PRO_TORQUE_ENABLE   = 64                  # RAM area

# Data Byte Length
LEN_PRO_GOAL_CURRENT     = 2
LEN_PRO_CURRENT_LIMIT    = 2

# Protocol version
PROTOCOL_VERSION         = 2.0                 # See which protocol version is used in the Dynamixel

# Default setting
DXL_ID                   = 7                   # Dynamixel ID
BAUDRATE                 = 57600
DEVICENAME               = '/dev/DYNAMIXEL'    # Check which port is being used on your controller

# Initialize PortHandler instance
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    os._exit(0)

# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    os._exit(0)

# Set operating mode to current control mode
packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_PRO_OPERATING_MODE, CURRENT_CONTROL_MODE)

# Set goal current
goal_current = 6  # 6mA
packetHandler.write2ByteTxRx(portHandler, DXL_ID, ADDR_PRO_GOAL_CURRENT, goal_current)

# Enable/Disable torque based on user input
while True:
    print("Type 'on' to enable torque, 'off' to disable torque, or 'exit' to quit:")
    cmd = input()
    if cmd == "on":
        # Enable Dynamixel Torque
        packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)
        print("Torque enabled")
    elif cmd == "off":
        # Disable Dynamixel Torque
        packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_PRO_TORQUE_ENABLE, TORQUE_DISABLE)
        print("Torque disabled")
    elif cmd == "exit":
        print("Exiting...")
        break
    else:
        print("Invalid command!")

# Close port
portHandler.closePort()
