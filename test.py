import serial
from dynamixel_sdk import *  # Uses Dynamixel SDK library

# Serial port settings
SERIAL_PORT = '/dev/ESP32'
SERIAL_BAUDRATE = 57600

# Dynamixel settings
ADDR_TORQUE_ENABLE = 64
ADDR_OPERATING_MODE = 11
ADDR_GOAL_VELOCITY = 104
OPERATING_MODE_VELOCITY = 1
DEVICENAME = '/dev/DYNAMIXEL'
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
        data = ser.readline().decode('utf-8').strip()
        motorSpeeds = [int(speed) for speed in data.split(',')]

        for i, speed in enumerate(motorSpeeds):
            dxl_id = i + 1
            dxl_packetHandler.write1ByteTxRx(dxl_portHandler, dxl_id, ADDR_OPERATING_MODE, OPERATING_MODE_VELOCITY)
            dxl_packetHandler.write1ByteTxRx(dxl_portHandler, dxl_id, ADDR_TORQUE_ENABLE, 1)
            dxl_packetHandler.write4ByteTxRx(dxl_portHandler, dxl_id, ADDR_GOAL_VELOCITY, speed)

# Close the Dynamixel port
dxl_portHandler.closePort()
