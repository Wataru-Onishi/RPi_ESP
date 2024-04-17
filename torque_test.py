import os
from dynamixel_sdk import *                    # Uses Dynamixel SDK library

# Control table address
ADDR_OPERATING_MODE    = 11                    # Operating mode address
ADDR_GOAL_CURRENT      = 102                   # Goal current address
ADDR_TORQUE_ENABLE     = 64                    # Torque enable address
ADDR_HARDWARE_ERROR    = 70                    # Hardware error status

# Data Byte Length
LEN_GOAL_CURRENT       = 2

# Protocol version
PROTOCOL_VERSION       = 2.0                   # Protocol version

# Default setting
DXL_ID                 = 7                     # Dynamixel ID
BAUDRATE               = 57600                 # Baudrate
DEVICENAME             = '/dev/DYNAMIXEL'                # Check which port is being used on your controller
                                                # ex) Windows: "COM1"   Linux: "/dev/ttyUSB0"

TORQUE_ENABLE          = 1                     # Value for enabling the torque
TORQUE_DISABLE         = 0                     # Value for disabling the torque
CURRENT_CONTROL_MODE   = 0                     # Current control mode is 0x00

# Initialize PortHandler instance
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Open port
if portHandler.openPort():
    print("Port opened successfully")
else:
    print("Failed to open the port")

# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Baudrate set successfully")
else:
    print("Failed to change the baudrate")

# Set operating mode to current control mode
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_OPERATING_MODE, CURRENT_CONTROL_MODE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Operating mode set to current control mode")

# Enable Dynamixel Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel has been successfully enabled")

# Write goal current
goal_current = 10   # mA
dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_CURRENT, goal_current)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Goal current has been set")

# Check for hardware error
dxl_comm_result, dxl_error, dxl_hw_error = packetHandler.read1ByteTxRx(portHandler, DXL_ID, ADDR_HARDWARE_ERROR)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Hardware error status: %d" % dxl_hw_error)

# Disable Dynamixel Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel has been successfully disabled")

# Close port
portHandler.closePort()
