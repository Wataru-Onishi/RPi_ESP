#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dynamixel_sdk import *  # Uses Dynamixel SDK library
import time  # for time.sleep()

# Control table address for Dynamixel X series
ADDR_TORQUE_ENABLE = 64
ADDR_OPERATING_MODE = 11  # Operating mode address
ADDR_GOAL_VELOCITY = 104  # Goal velocity address
OPERATING_MODE_VELOCITY = 1  # Value for velocity control mode

# Protocol version
PROTOCOL_VERSION = 2.0  # See which protocol version is used in the Dynamixel

# Default setting
DXL_IDS = [0, 1, 2, 3]  # Dynamixel IDs : 0 to 3
BAUDRATE = 57600  # Dynamixel default baudrate : 57600
DEVICENAME = '/dev/ttyUSB0'  # Check which port is being used on your controller

TORQUE_ENABLE = 1  # Value for enabling the torque
TORQUE_DISABLE = 0  # Value for disabling the torque
DXL_MOVING_SPEED = 100  # Dynamixel moving speed for continuous rotation

# Initialize PortHandler instance
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    quit()

# Set port baudrate
if not portHandler.setBaudRate(BAUDRATE):
    print("Failed to change the baudrate")
    quit()

# Change to velocity control mode and enable torque for all motors
for DXL_ID in DXL_IDS:
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_OPERATING_MODE, OPERATING_MODE_VELOCITY)
    if dxl_comm_result != COMM_SUCCESS:
        print(f"Failed to change operating mode to velocity control for DXL ID: {DXL_ID}")
        continue
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print(f"Failed to enable torque for DXL ID: {DXL_ID}")
        continue

# Set goal velocity for all motors
for DXL_ID in DXL_IDS:
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_VELOCITY, DXL_MOVING_SPEED)
    if dxl_comm_result != COMM_SUCCESS:
        print(f"Failed to set goal velocity for DXL ID: {DXL_ID}")
        continue

print("All Dynamixels are now rotating")
time.sleep(5)  # Rotate for 5 seconds

# Stop rotation and disable torque for all motors
for DXL_ID in DXL_IDS:
    dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_VELOCITY, 0)
    if dxl_comm_result != COMM_SUCCESS:
        print(f"Failed to stop the Dynamixel with ID: {DXL_ID}")
        continue
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print(f"Failed to disable torque for DXL ID: {DXL_ID}")
        continue

# Close port
portHandler.closePort()
