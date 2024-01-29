from serial.tools import list_ports
import serial

class TI:
    
    def read_serial(port):
        """Read data from serial port and return as string."""
        line = port.read(1000)
        return line.decode()

    def find_pico():
        #de PICO heeft altijd een vendor id en een product id. deze kunne we naar zoeken en dan wetten we welke port de PICO is op aangesloten is
        serial_port = list_ports.comports()
        pico_port = None
        for port in serial_port:
            if port.vid == 0x2E8A and port.pid == 0x0005:
                pico_port = port.device
                return pico_port
            
    def neo(value):
        if value == "0":
            data = "Red\r"
            TI.serial_port.write(data.encode())
        elif value == "1":
            data = "Green\r"
            TI.serial_port.write(data.encode())

    def send_serial(vaule):
        #verbind met de PICO met de juiste gegeves een maakt een as aan als serial_port.
        with serial.Serial(port=TI.find_pico(), baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1) as serial_port:
            data = f"{vaule}"
            if data == "0":
                data = "0\r"
                serial_port.write(data.encode())
                pico_output = TI.read_serial(serial_port)
                pico_output = pico_output.replace('\r\n', ' ')
            elif data == "1":
                data = "1\r"
                serial_port.write(data.encode())
            elif "status=" in data:
                data = f"{vaule}\r"
                serial_port.write(data.encode())
                pico_output = TI.read_serial(serial_port)
                pico_output = pico_output.replace('\r\n', ' ')
                print("[PICO] " + pico_output)
            else:
                data = f"lcd={vaule}\r"
                serial_port.write(data.encode())
                pico_output = TI.read_serial(serial_port)
                pico_output = pico_output.replace('\r\n', ' ')
                print("[PICO] " + pico_output)
            