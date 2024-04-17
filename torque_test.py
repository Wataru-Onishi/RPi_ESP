import os
from dynamixel_sdk import *

# Control table address
ADDR_PRO_GOAL_POSITION = 30
ADDR_PRO_PRESENT_POSITION = 36
ADDR_PRO_OPERATING_MODE = 11
ADDR_PRO_TORQUE_ENABLE = 64
ADDR_PRO_GOAL_CURRENT = 102
ADDR_PRO_CURRENT_LIMIT = 38

# Data Byte Length
LEN_PRO_GOAL_POSITION = 4
LEN_PRO_PRESENT_POSITION = 4
LEN_PRO_OPERATING_MODE = 1
LEN_PRO_TORQUE_ENABLE = 1
LEN_PRO_GOAL_CURRENT = 2
LEN_PRO_CURRENT_LIMIT = 2

# Protocol version
PROTOCOL_VERSION = 2.0

# Default setting
DXL_ID = 7
BAUDRATE = 57600
DEVICENAME = '/dev/DYNAMIXEL'

# Control mode
CURRENT_CONTROL_MODE = 0x0A
POSITION_CONTROL_MODE = 3

# Torque enable/disable
TORQUE_ENABLE = 1
TORQUE_DISABLE = 0

# Initialize PortHandler instance
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    os._exit(0)

# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    os._exit(0)

# Set operating mode to current control mode
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_PRO_OPERATING_MODE, CURRENT_CONTROL_MODE)
if dxl_comm_result != COMM_SUCCESS:
    print("Failed to change operating mode: %s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("Error occurred while changing operating mode: %s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Operating mode set to current control.")

# Main loop
try:
    while True:
        print("Type '1' to set current control mode and 6mA, '2' to move to position 1800, '3' to move to position 0, or 'exit' to quit:")
        cmd = input()
        if cmd == "1":
            # Enable Dynamixel Torque
            dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)
            if dxl_comm_result != COMM_SUCCESS:
                print("Failed to enable torque: %s" % packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("Error occurred while enabling torque: %s" % packetHandler.getRxPacketError(dxl_error))
            else:
                print("Torque enabled")

            # Set goal current to 6mA
            goal_current = 6
            dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL_ID, ADDR_PRO_GOAL_CURRENT, goal_current)
            if dxl_comm_result != COMM_SUCCESS:
                print("Failed to set goal current: %s" % packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("Error occurred while setting goal current: %s" % packetHandler.getRxPacketError(dxl_error))
            else:
                print("Goal current set to %d mA" % goal_current)

        elif cmd == "2":
            # Set operating mode to position control mode
            dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_PRO_OPERATING_MODE, POSITION_CONTROL_MODE)
            if dxl_comm_result != COMM_SUCCESS:
                print("Failed to change operating mode: %s" % packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("Error occurred while changing operating mode: %s" % packetHandler.getRxPacketError(dxl_error))
            else:
                print("Operating mode set to position control.")

            # Move to position 1800
            goal_position = 1800
            dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_PRO_GOAL_POSITION, goal_position)
            if dxl_comm_result != COMM_SUCCESS:
                print("Failed to move to position: %s" % packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("Error occurred while moving to position: %s" % packetHandler.getRxPacketError(dxl_error))
            else:
                print("Moving to position %d" % goal_position)

        elif cmd == "3":
            # Set operating mode to position control mode
            dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_PRO_OPERATING_MODE, POSITION_CONTROL_MODE)
            if dxl_comm_result != COMM_SUCCESS:
                print("Failed to change operating mode: %s" % packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("Error occurred while changing operating mode: %s" % packetHandler.getRxPacketError(dxl_error))
            else:
                print("Operating mode set to position control.")

            # Move to position 0
            goal_position = 0
            dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_PRO_GOAL_POSITION, goal_position)
            if dxl_comm_result != COMM_SUCCESS:
                print("Failed to move to position: %s" % packetHandler.getTxRxResult(dxl_comm_result))
            elif dxl_error != 0:
                print("Error occurred while moving to position: %s" % packetHandler.getRxPacketError(dxl_error))
            else:
                print("Moving to position %d" % goal_position)

        elif cmd == "exit":
            print("Exiting...")
            break

        else:
            print("Invalid command!")

except KeyboardInterrupt:
    print("Keyboard Interrupt. Exiting...")

# Close port
portHandler.closePort()
