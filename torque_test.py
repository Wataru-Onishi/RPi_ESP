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

TORQUE_ENABLE            = 1                   # Value for enabling the torque
TORQUE_DISABLE           = 0                   # Value for disabling the torque
CURRENT_CONTROL_MODE     = 0                   # Current Control mode

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
    os._exit(0)

# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    os._exit(0)

# Change Dynamixel ID to current control mode
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_PRO_OPERATING_MODE, CURRENT_CONTROL_MODE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Operating mode changed to current control mode.")

# Enable Dynamixel Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel has been successfully enabled")

# Write goal current
goal_current = 10  # 10mA
dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL_ID, ADDR_PRO_GOAL_CURRENT, goal_current)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Goal current has been set")

# Disable Dynamixel Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_PRO_TORQUE_ENABLE, TORQUE_DISABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel has been successfully disabled")

# Close port
portHandler.closePort()
