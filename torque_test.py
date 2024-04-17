import os
import time
from dynamixel_sdk import *                    # Uses Dynamixel SDK library

# Control table address
ADDR_PRO_LED_RED                = 65           # Control table address is different in Dynamixel model

# Data Byte Length
LEN_PRO_LED_RED                 = 1            # Data length

# Protocol version
PROTOCOL_VERSION                = 2.0          # See which protocol version is used in the Dynamixel

# Default setting
DXL_ID                          = 7            # Dynamixel ID : 7
BAUDRATE                        = 57600        # Dynamixel default baudrate : 57600
DEVICENAME                      = '/dev/DYNAMIXEL' # Check which port is being used on your controller

# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
# Set the protocol version
# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    os.system('pause')
    quit()

# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    os.system('pause')
    quit()

# Turn LED on and off repeatedly.
try:
    while True:
        # Turn LED on
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_PRO_LED_RED, 1)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        else:
            print("Dynamixel has been successfully turned on")

        time.sleep(1)   # 1 second pause

        # Turn LED off
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_PRO_LED_RED, 0)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))
        else:
            print("Dynamixel has been successfully turned off")

        time.sleep(1)   # 1 second pause

except KeyboardInterrupt:
    # Close port
    portHandler.closePort()
    print("Port closed")
    print("Program terminated")
