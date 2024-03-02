#!/usr/bin/env python
# -*- coding: utf-8 -*-

import serial
from dynamixel_sdk import *  # Uses Dynamixel SDK library
import time  # for time.sleep()

# Serial port settings
SERIAL_PORT = '/dev/ttyUSB2'  # Adjust this to your serial port
SERIAL_BAUDRATE = 57600

# Dynamixel settings
# これらの行をプログラムの適切な場所（通常は他の定義の近く）に追加します
TORQUE_ENABLE = 1     # トルクを有効にするための値
TORQUE_DISABLE = 0    # トルクを無効にするための値

ADDR_TORQUE_ENABLE = 64
ADDR_OPERATING_MODE = 11
ADDR_GOAL_VELOCITY = 104
OPERATING_MODE_VELOCITY = 1
DXL_IDS = [1, 2, 3, 4]
DXL_MOVING_SPEED = 200  # Adjust speed here
DEVICENAME = '/dev/ttyUSB0'
PROTOCOL_VERSION = 2.0
BAUDRATE = 57600

# Initialize PortHandler and PacketHandler instances for Dynamixel
dxl_portHandler = PortHandler(DEVICENAME)
dxl_packetHandler = PacketHandler(PROTOCOL_VERSION)

# Open the Dynamixel port
if dxl_portHandler.openPort():
    print("Dynamixel port opened successfully")
else:
    print("Failed to open the Dynamixel port")
    quit()

# Set Dynamixel port baudrate
if not dxl_portHandler.setBaudRate(BAUDRATE):
    print("Failed to change the Dynamixel baudrate")
    quit()

# Initialize and open the serial port for receiving commands
ser = serial.Serial(SERIAL_PORT, SERIAL_BAUDRATE, timeout=1)
print("Serial port opened for commands")

while True:
    if ser.in_waiting > 0:
        command = ser.read().decode('utf-8')

        if command == '0':
            print("Command to rotate received")
            for DXL_ID in DXL_IDS:
                # Set to velocity control mode
                dxl_packetHandler.write1ByteTxRx(dxl_portHandler, DXL_ID, ADDR_OPERATING_MODE, OPERATING_MODE_VELOCITY)
                # Enable torque
                dxl_packetHandler.write1ByteTxRx(dxl_portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
                # Set goal velocity
                dxl_packetHandler.write4ByteTxRx(dxl_portHandler, DXL_ID, ADDR_GOAL_VELOCITY, DXL_MOVING_SPEED)

        elif command == '1':
            print("Command to stop received")
            for DXL_ID in DXL_IDS:
                # Set goal velocity to 0 to stop
                dxl_packetHandler.write4ByteTxRx(dxl_portHandler, DXL_ID, ADDR_GOAL_VELOCITY, 0)
                # Disable torque
                dxl_packetHandler.write1ByteTxRx(dxl_portHandler, DXL_ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)

# Close the Dynamixel port
dxl_portHandler.closePort()
