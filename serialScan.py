import serial

ser = 0


# Function to Initialize the Serial Port
def init_serial():
    COMNUM = 1  # Enter Your COM Port Number Here.
    global ser  # Must be declared in Each Function
    ser = serial.Serial()
    ser.baudrate = 9600  # 115200
    # ser.port = COMNUM - 1   #COM Port Name Start from 0
    ser.port = '/dev/ttyUSB0'  # If Using Linux # '/dev/ttyUSB0' #If Using Linux

    ser.timeout = 10
    ser.open()  # Opens SerialPort

    # print port open or closed
    if ser.isOpen():
        print('Open: ' + ser.portstr)


init_serial()

while 1:
    bytes = ser.readline()  # Read from Serial Port
    print(bytes.encode("hex"))  # Print What is Read from Port
