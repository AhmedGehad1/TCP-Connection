import socket
import json
import redis

# Define constants
HOST_IP = "Ahmed"
HOST_PORT = 12345
BYTESIZE = 1024

# Create a server side socket using IPV4 (AF_INET) and TCP (SOCK_STREAM)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind our new socket to a tuple (IP Address, Port Address)
server_socket.bind((HOST_IP, HOST_PORT))

# Put the socket into listening mode to listen for any possible connections
server_socket.listen()

print('Server is running...\n')

####Redis setup
r = redis.Redis(
    host='redis-16661.c55.eu-central-1-1.ec2.redns.redis-cloud.com',
    port= 16661,
    password= 'iLi2QxUtJwj9PPVG9AbXWNOTF5aD5qO2',
    decode_responses = True
)

def handle_client(client):
    while True:
        message = client.recv(BYTESIZE).decode()
        # message contains patient vital signs in JSON format
        vital_signs = json.loads(message)
        print(f"Received vital signs from {vital_signs['Name']}:")
        print(json.dumps(vital_signs, indent=4))

        # Store vital signs data in Redis
        # Use a unique key, for example, based on the patient's name
        key = f"vital_signs:{vital_signs['id']}"
        # Convert the vital signs dictionary to a JSON string
        data_to_store = json.dumps(vital_signs)
        # Store the data in Redis under the specified key
        r.set(key, data_to_store)

print('Server is running and listening ...')
client, address = server_socket.accept()
print(f'Connection is established with {str(address)}')
handle_client(client)