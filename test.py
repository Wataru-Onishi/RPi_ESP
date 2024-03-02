import serial
from dynamixel_sdk import *  # Uses Dynamixel SDK library

# Serial port settings
SERIAL_PORT = '/dev/ttyUSB0'
SERIAL_BAUDRATE = 57600

# Dynamixel settings
ADDR_TORQUE_ENABLE = 64
ADDR_OPERATING_MODE = 11
ADDR_GOAL_VELOCITY = 104
OPERATING_MODE_VELOCITY = 1
DEVICENAME = '/dev/ttyUSB1'
PROTOCOL_VERSION = 2.0
BAUDRATE = 57600

# Initialize PortHandler and PacketHandler instances for Dynamixel
dxl_portHandler = PortHandler(DEVICENAME)
dxl_packetHandler = PacketHandler(PROTOCOL_VERSION)

# Base speed settings for each motor
dxl_base_speeds = {
    1: 100,  # Base speed for motor ID 1
    2: 100,  # Base speed for motor ID 2
    3: 100,  # Base speed for motor ID 3
    4: 100   # Base speed for motor ID 4
}

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
        command = ser.read().decode('utf-8').strip()

        if command == '0':  # Stop
            print("Command to stop received")
            for dxl_id in dxl_base_speeds.keys():
                dxl_packetHandler.write4ByteTxRx(dxl_portHandler, dxl_id, ADDR_GOAL_VELOCITY, 0)
                dxl_packetHandler.write1ByteTxRx(dxl_portHandler, dxl_id, ADDR_TORQUE_ENABLE, 0)

        elif command == '1':  # Forward
            print("Command for forward rotation received")
            for dxl_id, speed in dxl_base_speeds.items():
                dxl_packetHandler.write1ByteTxRx(dxl_portHandler, dxl_id, ADDR_OPERATING_MODE, OPERATING_MODE_VELOCITY)
                dxl_packetHandler.write1ByteTxRx(dxl_portHandler, dxl_id, ADDR_TORQUE_ENABLE, 1)
                dxl_packetHandler.write4ByteTxRx(dxl_portHandler, dxl_id, ADDR_GOAL_VELOCITY, speed)

        elif command == '2':  # Reverse
            print("Command for reverse rotation received")
            for dxl_id, speed in dxl_base_speeds.items():
                dxl_packetHandler.write1ByteTxRx(dxl_portHandler, dxl_id, ADDR_OPERATING_MODE, OPERATING_MODE_VELOCITY)
                dxl_packetHandler.write1ByteTxRx(dxl_portHandler, dxl_id, ADDR_TORQUE_ENABLE, 1)
                dxl_packetHandler.write4ByteTxRx(dxl_portHandler, dxl_id, ADDR_GOAL_VELOCITY, -speed)

# Close the Dynamixel port
dxl_portHandler.closePort()
