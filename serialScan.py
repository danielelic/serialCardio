import serial
#Can be Downloaded from this Link
#https://pypi.python.org/pypi/pyserial

#Global Variables
ser = 0

#Function to Initialize the Serial Port
def init_serial():
    COMNUM = 1          #Enter Your COM Port Number Here.
    global ser          #Must be declared in Each Function
    ser = serial.Serial()
    ser.baudrate = 9600 # 115200
    #ser.port = COMNUM - 1   #COM Port Name Start from 0

    ser.port = '/dev/ttyUSB0' #If Using Linux # '/dev/ttyUSB0' #If Using Linux

    #Specify the TimeOut in seconds, so that SerialPort
    #Doesn't hangs
    ser.timeout = 10
    ser.open()          #Opens SerialPort

    # print port open or closed
    if ser.isOpen():
        print 'Open: ' + ser.portstr
#Function Ends Here


#Call the Serial Initilization Function, Main Program Starts from here
init_serial()

while 1:
    bytes = ser.readline()  #Read from Serial Port
    print bytes.encode("hex")      #Print What is Read from Port

#Ctrl+C to Close Python Window
