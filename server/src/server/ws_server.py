import socket
import time
import csv
from threading import Timer

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 5002))
s.listen(5)
print('Server is running ...')

def background_controller(clientsocket):
    with open('distances_data.csv', 'r') as file:
        csv_reader = csv.reader(file)
        distances_data = "\n".join(",".join(row) for row in csv_reader)

    clientsocket.send(bytes(distances_data, "utf-8"))
    Timer(5, background_controller, args=(clientsocket,)).start()

try:
    while True:
        clientsocket, address = s.accept()
        print(f"Connection from {address} has been established.")
        background_controller(clientsocket)

except KeyboardInterrupt:
    print("Server is shutting down...")
finally:
    s.close()


