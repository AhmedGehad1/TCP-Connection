# TCP-Connection
Simple TCP Connection with GUI (Patient Monitor)

# TCP Connection with GUI (Patient Monitor)

This project implements a patient monitoring system using TCP/IP communication for data transmission and a Qt-based graphical user interface for real-time visualization.

## Features

### Client (Sender)

- **Sending Vital Signs**: Sends patient’s live vital signs to the server using TCP connection.
  - Ensure `DEST_IP = "Ahmed"` is set to your PC's localhost.
  - Connects client socket to the server specified by the destination IP and port.
- **Patient Class**: Defines a `Patient` class with attributes such as id, name, age, heart rate, systolic blood pressure, and diastolic blood pressure.
  - `generate_vital_signs()`: Generates random vital signs for a patient.
  - `get_vital_signs()`: Returns vital signs in JSON format.
- **Client Send Function**: Sends vital signs data in JSON format via the client socket in a loop, with a 2-second interval between transmissions.

### Server (Receiver)

- **Receiving Vital Signs**: Receives vital signs data from clients and stores it in a Redis database.
  - Ensure `HOST_IP = "Ahmed"` is set to your PC's localhost.
  - Sets up a server-side socket and binds it to the specified IP address and port.
  - Creates and connects to an online Redis database, storing vital signs under unique keys.
- **Handling Clients**: `handle_client(client)`: Receives JSON-formatted data from clients, decodes it, and stores vital signs in Redis.
- **Main Server Loop**: Listens for incoming connections, accepting and handling clients using the `handle_client` function.

### Qt Creator GUI

- **Live Plotting Graph**: Displays live graphs of vital signs data using Matplotlib embedded in a Qt application.
  - `LivePlotWidget` class inherits from `FigureCanvas` for live plotting.
  - Initializes plots for heart rate and blood pressure, fetching data from Redis.
  - User interface managed by Qt, allowing selection of vital sign type (heart rate or blood pressure) and patient ID for dynamic plotting.
  - Supports real-time updates based on Redis data fetches.

### User Interface

- **Usage Instructions**: Steps on effectively using the patient monitor Qt application:
  - Insert correct patient ID.
  - Select vital sign (heart rate or blood pressure) from the combo box.
  - Press submit to display the live graph.
  - Alternate between vital signs using the combo box.
  - Change patient ID to view another patient’s vital signs.

## Dependencies

- Python 3.x
- Qt Creator
- Matplotlib
- Redis
- Other necessary Python libraries

## Setup Instructions

1. Set up Redis database and configure connection details in the code.
2. Run `server.py` to start the server.
3. Run `client.py` to start sending vital signs data.
4. Launch Qt application (`python main.py`) to visualize live patient vital signs.

More details are in the pdf

https://github.com/AhmedGehad1/TCP-Connection/assets/125567504/8c8e2baf-c77b-411f-9667-ffd7a5b5177b

