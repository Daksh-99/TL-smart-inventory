# import serial
# import time
# import requests

# # Serial port for RFID scanner
# rfid_port = 'COM3'  # Change this to your RFID scanner's port (e.g., COM3 on Windows)

# # Local website URL for sending data
# local_website_url = 'http://localhost:8000'

# # Initialize the serial connection to the RFID scanner
# try:
#     rfid_reader = serial.Serial(rfid_port, baudrate=9600)
# except serial.SerialException:
#     print(f"Failed to connect to {rfid_port}. Please check the port.")
#     exit(1)

# while True:
#     try:
#         # Read data from the RFID scanner
#         rfid_data = rfid_reader.readline().strip().decode('utf-8')

#         # Send the RFID tag to the local website
#         response = requests.post(local_website_url, data={'rfid_tag': rfid_data})
        
#         if response.status_code == 200:
#             print(f"RFID tag sent to the local website successfully")
#         else:
#             print(f"Failed to send RFID tag to the local website with status code {response.status_code}")
    
#     except Exception as e:
#         print(f"An error occurred: {str(e)}")

#     time.sleep(1)  # Adjust the delay as needed

# # Close the RFID port when done
# rfid_reader.close()


import requests

rfid_tag = "0313832938"  # Replace with the scanned RFID tag
rfid_url = "http://127.0.0.1:8000/"  # Include the full URL

data = {'rfid_tag': rfid_tag}
response = requests.post(rfid_url, data=data)

if response.status_code == 200:
    response_data = response.json()
    if response_data.get('success'):
        student_data = response_data.get('student')
        print("RFID tag sent to the server")
        # Now, you can use the student data as needed
        print(student_data)
    else:
        print("RFID tag not found")
else:
    print(f"Failed to send RFID tag with status code {response.status_code}")

