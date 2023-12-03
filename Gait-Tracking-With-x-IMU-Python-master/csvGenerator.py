import serial
import csv

# Open the serial port (update 'COMx' with your specific port)
ser = serial.Serial('COM4', baudrate=115200, timeout=1)

# Create and open the CSV file for writing
csv_file_path = 'rocketData.csv'
with open(csv_file_path, 'w', newline='') as csv_file:
    # Define the CSV header
    fieldnames = ['Packet number', 'Gyroscope X (deg/s)', 'Gyroscope Y (deg/s)', 'Gyroscope Z (deg/s)',
                  'Accelerometer X (g)', 'Accelerometer Y (g)', 'Accelerometer Z (g)',
                  'Magnetometer X (G)', 'Magnetometer Y (G)', 'Magnetometer Z (G)']
    
    # Create a CSV writer
    csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    
    # Write the header to the CSV file
    csv_writer.writeheader()
    
    # Read data from the serial port and write to the CSV file
    packet_number = 1
    while True:
        # Read a line from the serial port
        line = ser.readline().decode('utf-8').strip()
        
        # Split the line into individual values
        values = line.split(' ')
        
        # Check if the line has the correct number of values
        if len(values) == len(fieldnames) - 1:
            # Create a dictionary with the data
            data_dict = {'Packet number': packet_number}
            for fieldname, value in zip(fieldnames[1:], values):
                data_dict[fieldname] = float(value)
            
            # Write the data to the CSV file
            csv_writer.writerow(data_dict)
            
            # Increment the packet number
            packet_number += 1

# Close the serial port
ser.close()
