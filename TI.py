from serial.tools import list_ports
import serial

class TI:
    
    def read_serial(port):
        """Read data from serial port and return as string."""
        line = port.read(1000)
        return line.decode()

    def find_pico():
        serial_ports = list_ports.comports()
        pico_port = None
        for port in serial_ports:
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
    
    def lcd(value):
        value = str(f"lcd={value}")
        TI.serial_port.write(value.encode())

    def send_serial(vaule):
        with serial.Serial(port=TI.find_pico(), baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1) as serial_port:
            data = f"{vaule}\r"
            if data == 'off':
                # Turn led off by sending a '0'
                data = "0\r"
                serial_port.write(data.encode())
                pico_output = TI.read_serial(serial_port)
                pico_output = pico_output.replace('\r\n', ' ')
                print("[PICO] " + pico_output)
            elif data == 'on':
                # Turn led on by sending a '1'
                data = "1\r"
                serial_port.write(data.encode())
                pico_output = TI.read_serial(serial_port)
                pico_output = pico_output.replace('\r\n', ' ')
                print("[PICO] " + pico_output)
            elif data == "lcd":
                data = f"lcd={vaule}\r"
                serial_port.write(data.encode())
                pico_output = TI.read_serial(serial_port)
                pico_output = pico_output.replace('\r\n', ' ')
                print("[PICO] " + pico_output)