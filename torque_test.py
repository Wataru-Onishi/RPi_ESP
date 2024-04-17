import dynamixel_sdk as dxl

# Control table address
ADDR_OPERATING_MODE = 11
ADDR_CURRENT_LIMIT = 38
ADDR_GOAL_POSITION = 30
ADDR_PRESENT_POSITION = 36

# Protocol version
PROTOCOL_VERSION = 2.0

# Default setting
DXL_ID = 7  # DYNAMIXEL ID
BAUDRATE = 57600  # Default baudrate
DEVICENAME = '/dev/DYNAMIXEL'  # Default device name

# Initialize PortHandler instance
portHandler = dxl.PortHandler(DEVICENAME)

# Initialize PacketHandler instance
packetHandler = dxl.PacketHandler(PROTOCOL_VERSION)

# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    quit()

# Set baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    quit()

# Function to set operating mode to current control mode
def set_current_control_mode():
    dxl_comm_result, _ = packetHandler.write1ByteTxRx(portHandler, DXL_ID, ADDR_OPERATING_MODE, 0)
    return dxl_comm_result == dxl.COMM_SUCCESS

# Function to set current limit
def set_current_limit(current_limit):
    dxl_comm_result, _ = packetHandler.write2ByteTxRx(portHandler, DXL_ID, ADDR_CURRENT_LIMIT, current_limit)
    return dxl_comm_result == dxl.COMM_SUCCESS

# Function to set goal position
def set_goal_position(goal_position):
    dxl_comm_result, _ = packetHandler.write4ByteTxRx(portHandler, DXL_ID, ADDR_GOAL_POSITION, goal_position)
    return dxl_comm_result == dxl.COMM_SUCCESS

# Function to get present position
def get_present_position():
    present_position, _, _ = packetHandler.read4ByteTxRx(portHandler, DXL_ID, ADDR_PRESENT_POSITION)
    return present_position

# Main code
try:
    while True:
        command = input("Enter command (1: Set current control mode, 2: Move to position 1800, 3: Move to position 0, exit: Exit program): ")
        
        if command == '1':
            if set_current_control_mode():
                print("Changed to current control mode")
                set_current_limit(6)  # Set current limit to 6mA
            else:
                print("Failed to change to current control mode")

        elif command == '2':
            set_goal_position(1800)  # Move to position 1800
            print("Moving to position 1800")

        elif command == '3':
            set_goal_position(0)  # Move to position 0
            print("Moving to position 0")

        elif command == 'exit':
            break

        else:
            print("Invalid command")

except KeyboardInterrupt:
    print("\nProgram interrupted")

# Close port
portHandler.closePort()
