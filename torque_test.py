from dynamixel_sdk import *                    # Uses Dynamixel SDK library
# Control table address
ADDR_PRO_CURRENT_LIMIT = 38                    # EEPROM area to limit peak current
ADDR_PRO_GOAL_CURRENT = 102                    # Address of Goal Current
ADDR_PRO_TORQUE_ENABLE = 64                    # Address of Torque Enable
ADDR_PRO_OPERATING_MODE = 11                   # Operating Mode Address

# Data Byte Length
LEN_PRO_GOAL_CURRENT = 2

# Protocol version
PROTOCOL_VERSION = 2.0                         # Protocol version

# Default setting
DXL_ID = 7                                     # Dynamixel ID
BAUDRATE = 57600                               # Dynamixel default baudrate : 57600
DEVICENAME = '/dev/DYNAMIXEL'                  # Check which port is being used on your controller

TORQUE_ENABLE = 1                              # Value for enabling the torque
TORQUE_DISABLE = 0                             # Value for disabling the torque
CURRENT_CONTROL_MODE = 0                       # Current Control mode
GOAL_CURRENT_VALUE = 10                        # Goal current in mA (10 mA)
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
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    quit()
# Set operating mode to current-based control
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_PRO_OPERATING_MODE, CURRENT_CONTROL_MODE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Operating mode changed to current control mode.")

# Enable Dynamixel Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_PRO_TORQUE_ENABLE, TORQUE_ENABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel has been successfully enabled.")
# Write goal current
dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL_ID, ADDR_PRO_GOAL_CURRENT, GOAL_CURRENT_VALUE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Goal current has been set to %d mA" % GOAL_CURRENT_VALUE)

# Disable Dynamixel Torque
dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_PRO_TORQUE_ENABLE, TORQUE_DISABLE)
if dxl_comm_result != COMM_SUCCESS:
    print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
elif dxl_error != 0:
    print("%s" % packetHandler.getRxPacketError(dxl_error))
else:
    print("Dynamixel has been successfully disabled.")

# Close port
portHandler.closePort()
