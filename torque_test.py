import os
from dynamixel_sdk import *                    # Uses Dynamixel SDK library

# Control table address
ADDR_PRO_CURRENT_LIMIT   = 38                  # EEPROM area
ADDR_PRO_GOAL_POSITION   = 116                 # RAM area for XM430-W350
ADDR_PRO_OPERATING_MODE  = 11                  # EEPROM area
ADDR_PRO_TORQUE_ENABLE   = 64                  # RAM area

# Data Byte Length
LEN_PRO_GOAL_POSITION    = 4
LEN_PRO_CURRENT_LIMIT    = 2

# Protocol version
PROTOCOL_VERSION         = 2.0                 # See which protocol version is used in the Dynamixel

# Default setting
DXL_ID                   = 7                   # Dynamixel ID
BAUDRATE                 = 57600
DEVICENAME               = '/dev/DYNAMIXEL'    # Check which port is being used on your controller

POSITION_CONTROL_MODE    = 3                   # Position Control mode
TORQUE_ENABLE            = 1                   # Value for enabling the torque
TORQUE_DISABLE           = 0                   # Value for disabling the torque

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

# Set operating mode to position control mode
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_PRO_OPERATING_MODE, POSITION_CONTROL_MODE)
if dxl_comm_result != COMM_SUCCESS:
    print("Failed to change operating mode: %s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("Error occurred while changing operating mode: %s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Operating mode set to position control.")

# Set goal position to 1800 when torque is turned off
def set_goal_position_1800():
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_PRO_GOAL_POSITION, 1800)
    if dxl_comm_result != COMM_SUCCESS:
        print("Failed to set goal position: %s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("Error occurred while setting goal position: %s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("Goal position set to 1800")

# Set torque enable
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("Failed to enable torque: %s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("Error occurred while enabling torque: %s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Torque enabled")

# Main loop
while True:
    print("Type 'off' to disable torque and set goal position to 1800, or 'exit' to quit:")
    cmd = input()
    if cmd == "off":
        set_goal_position_1800()
        # Disable Dynamixel Torque
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_PRO_TORQUE_ENABLE, TORQUE_DISABLE)
        if dxl_comm_result != COMM_SUCCESS:
            print("Failed to disable torque: %s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("Error occurred while disabling torque: %s" % packetHandler.getRxPacketError(dxl_error))
        else:
            print("Torque disabled")
    
    elif cmd == "exit":
        print("Exiting...")
        # Disable Dynamixel Torque before exiting
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_PRO_TORQUE_ENABLE, TORQUE_DISABLE)
        if dxl_comm_result != COMM_SUCCESS:
            print("Failed to disable torque: %s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("Error occurred while disabling torque: %s" % packetHandler.getRxPacketError(dxl_error))
        else:
            print("Torque disabled")
        break
    
    else:
        print("Invalid command!")

# Close port
portHandler.closePort()
