#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dynamixel_sdk import *                    # Uses Dynamixel SDK library
import time                                    # for time.sleep()

# Control table address for Dynamixel X series
ADDR_TORQUE_ENABLE      = 64
ADDR_OPERATING_MODE     = 11                   # Operating mode address
ADDR_GOAL_VELOCITY      = 104                  # Goal velocity address
OPERATING_MODE_VELOCITY = 1                    # Value for velocity control mode

# Protocol version
PROTOCOL_VERSION = 2.0                         # See which protocol version is used in the Dynamixel

# Default setting
DXL_ID = 1                                      # Dynamixel ID : 1
BAUDRATE = 57600                                # Dynamixel default baudrate : 57600
DEVICENAME = '/dev/ttyUSB0'                     # Check which port is being used on your controller

TORQUE_ENABLE = 1                               # Value for enabling the torque
TORQUE_DISABLE = 0                              # Value for disabling the torque
DXL_MOVING_SPEED = 200                          # Dynamixel moving speed for continuous rotation

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

# Change to velocity control mode
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_OPERATING_MODE, OPERATING_MODE_VELOCITY)
if dxl_comm_result != COMM_SUCCESS:
    print("Failed to change operating mode to velocity control")
    quit()

# Enable Dynamixel Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("Failed to enable torque")
    quit()

# Set goal velocity
dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_VELOCITY, DXL_MOVING_SPEED)
if dxl_comm_result != COMM_SUCCESS:
    print("Failed to set goal velocity")
    quit()

print("Dynamixel is now rotating")
time.sleep(5)  # Rotate for 5 seconds

# Stop rotation
dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_VELOCITY, 0)
if dxl_comm_result != COMM_SUCCESS:
    print("Failed to stop the Dynamixel")
    quit()

# Disable Dynamixel Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("Failed to disable torque")
    quit()

# Close port
portHandler.closePort()
