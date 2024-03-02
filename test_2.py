import serial
from dynamixel_sdk import *  # Uses Dynamixel SDK library
import time

# Dynamixel settings
ADDR_TORQUE_ENABLE = 64
ADDR_OPERATING_MODE = 11
ADDR_GOAL_VELOCITY = 104
OPERATING_MODE_VELOCITY = 1
BAUDRATE = 57600
DEVICENAME = '/dev/ttyUSB1'
PROTOCOL_VERSION = 2.0

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
ser = serial.Serial('/dev/ttyUSB0', 57600, timeout=1)  # Adjust serial port
print("Serial port opened for commands")

while True:
    if ser.in_waiting > 0:
        message = ser.readline().decode('utf-8').strip()  # Read the incoming message
        parts = message.split(":")  # Split message by ':'
        if len(parts) == 2:
            try:
                dxl_id = int(parts[0])  # Extract Dynamixel ID
                dxl_speed = int(parts[1])  # Extract speed
                
                # Set to velocity control mode
                dxl_packetHandler.write1ByteTxRx(dxl_portHandler, dxl_id, ADDR_OPERATING_MODE, OPERATING_MODE_VELOCITY)
                
                # Enable torque
                dxl_packetHandler.write1ByteTxRx(dxl_portHandler, dxl_id, ADDR_TORQUE_ENABLE, 1)
                
                # Set goal velocity
                dxl_packetHandler.write4ByteTxRx(dxl_portHandler, dxl_id, ADDR_GOAL_VELOCITY, dxl_speed)
                print(f"Motor {dxl_id} set to speed {dxl_speed}")
            except ValueError:
                print("Invalid command received")
