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
DEVICENAME             = 'COM1'                # Check which port is being used on your controller

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
    exit()

# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Baudrate set successfully")
else:
    print("Failed to change the baudrate")
    exit()

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

# Read Hardware Error Status
dxl_comm_result, dxl_error, dxl_hw_error = packetHandler.read1ByteTxRx(portHandler, DXL_ID, ADDR_HARDWARE_ERROR)
if dxl_comm_result != COMM_SUCCESS:
    print("Failed to read hardware error status: %s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("Communication error when reading hardware error status: %s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Hardware error status: %d" % dxl_hw_error)
    if dxl_hw_error != 0:
        print("Error Code: %d -> %s" % (dxl_hw_error, decode_hardware_error(dxl_hw_error)))

def decode_hardware_error(error_code):
    errors = []
    if error_code & 1: errors.append("Input Voltage Error")
    if error_code & 2: errors.append("Overheating Error")
    if error_code & 4: errors.append("Motor Encoder Error")
    if error_code & 8: errors.append("Electrical Shock Error")
    if error_code & 16: errors.append("Overload Error")
    return ", ".join(errors)

# Write goal current
goal_current = 1000   # mA
dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_CURRENT, goal_current)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Goal current has been set")

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
