import os
from dynamixel_sdk import *                    # Uses Dynamixel SDK library

# Control table address
ADDR_PRO_CURRENT_LIMIT   = 38                  # EEPROM area
ADDR_PRO_GOAL_POSITION   = 116                 # RAM area for position control mode
ADDR_PRO_GOAL_CURRENT    = 102                 # RAM area for current control mode
ADDR_PRO_OPERATING_MODE  = 11                  # EEPROM area
ADDR_PRO_TORQUE_ENABLE   = 64                  # RAM area

# Data Byte Length
LEN_PRO_GOAL_CURRENT     = 2
LEN_PRO_GOAL_POSITION    = 4

# Protocol version
PROTOCOL_VERSION         = 2.0                 # See which protocol version is used in the Dynamixel

# Default setting
DXL_ID                   = 7                   # Dynamixel ID
BAUDRATE                 = 57600
DEVICENAME               = '/dev/DYNAMIXEL'    # Check which port is being used on your controller

# Control modes
POSITION_CONTROL_MODE    = 3                   # Position Control mode
CURRENT_CONTROL_MODE     = 0x0A                # Current Control mode (0x0A for XM430-W350)
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

# Main loop
while True:
    print("Type '1' to enable torque and set current to 6mA, '2' to switch to position control mode and set goal position to 1800, 'exit' to quit:")
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

        # Set operating mode to current control mode
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_PRO_OPERATING_MODE, CURRENT_CONTROL_MODE)
        if dxl_comm_result != COMM_SUCCESS:
            print("Failed to change operating mode: %s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("Error occurred while changing operating mode: %s" % packetHandler.getRxPacketError(dxl_error))
        else:
            print("Operating mode set to current control.")

        # Set goal current to 6mA
        goal_current = 6  # 6mA
        dxl_comm_result, dxl_error = packetHandler.write2ByteTxRx(portHandler, DXL_ID, ADDR_PRO_GOAL_CURRENT, goal_current)
        if dxl_comm_result != COMM_SUCCESS:
            print("Failed to set goal current: %s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("Error occurred while setting goal current: %s" % packetHandler.getRxPacketError(dxl_error))
        else:
            print("Goal current set to %d mA" % goal_current)
    
    elif cmd == "2":
        # Switch to position control mode
        dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_PRO_OPERATING_MODE, POSITION_CONTROL_MODE)
        if dxl_comm_result != COMM_SUCCESS:
            print("Failed to switch to position control mode: %s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("Error occurred while switching to position control mode: %s" % packetHandler.getRxPacketError(dxl_error))
        else:
            print("Switched to position control mode")
        
        # Set goal position to 1800
        goal_position = 1800
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_PRO_GOAL_POSITION, goal_position)
        if dxl_comm_result != COMM_SUCCESS:
            print("Failed to set goal position: %s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("Error occurred while setting goal position: %s" % packetHandler.getRxPacketError(dxl_error))
        else:
            print("Goal position set to %d" % goal_position)
    
    elif cmd == "exit":
        print("Exiting...")
        break
    
    else:
        print("Invalid command!")

# Close port
portHandler.closePort()
