import socket
import random
import time
import json

# Define constants to be used
DEST_IP = "Ahmed"
DEST_PORT = 12345
BYTESIZE = 1024

# Create a client side socket using IPV4 (AF_INET) and TCP (SOCK_STREAM)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to a server located at a given IP and Port
client_socket.connect((DEST_IP, DEST_PORT))

class Patient:
    def __init__(self, id, name, age):
        self.id = id
        self.name = name
        self.age = age
        self.heart_rate = 0
        self.systolic_bp = 0
        self.diastolic_bp = 0
    
    def generate_vital_signs(self):
        # Generate random heart rate between 60 and 100 beats per minute
        self.heart_rate = random.randint(60, 100)
        
        # Generate random systolic blood pressure between 90 and 120 mmHg
        self.systolic_bp = random.randint(90, 120)
        
        # Generate random diastolic blood pressure between 60 and 80 mmHg
        self.diastolic_bp = random.randint(60, 80)
        
    def get_vital_signs(self):
        return {
            "id": self.id,
            "Name": self.name,
            "Age": self.age,
            "Heart Rate": self.heart_rate,
            "Systolic BP": self.systolic_bp,
            "Diastolic BP": self.diastolic_bp
        }

# Create instances of patients
patient1 = Patient(1200387,"Ahmed Doe", 35)
patient2 = Patient(1100123,"Jane Smith", 45)

# List of patients
patients = [patient1, patient2]

def client_send():
    while True:
        for patient in patients:
            patient.generate_vital_signs()
            vital_signs = patient.get_vital_signs()
            message = json.dumps(vital_signs)  # Convert to JSON format
            client_socket.send(message.encode())
            time.sleep(2)  # Delay between each loop

client_send()
