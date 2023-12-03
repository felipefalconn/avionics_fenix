import serial

def parse_serial_data(serial_input):
    try:
        # Split the input string into individual values
        yaw, pitch, roll = map(float, serial_input.strip().split())

        # Process or manipulate the data as needed
        # For example, print the values
        print(f"Yaw: {yaw}, Pitch: {pitch}, Roll: {roll}")

        # You can perform other operations with the data here

    except ValueError as e:
        print(f"Error parsing serial data: {e}")

# Example usage with a serial port
ser = serial.Serial('COM7', 115200)  # Adjust the port and baud rate accordingly

while True:
    serial_input_data = ser.readline().decode('utf-8')
    parse_serial_data(serial_input_data)