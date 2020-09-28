import socket
import threading
import pyaudio
import time
import logging

from tkinter import *
from tkinter import ttk


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


root = Tk()

var_ip = StringVar()
var_port = StringVar()
var_destinated_port = StringVar()
var_connected_to = StringVar()
var_server_status = StringVar()
var_client_status = StringVar()
var_in_status = StringVar()

# test
var_ip.set("192.168.8.148")
var_destinated_port.set("6000")
var_connected_to.set("Not connected")
var_server_status.set("Server Stopped")
var_client_status.set("Client Stopped                                            ")
var_port.set("")
var_in_status.set("1")

chunk_size = 1024
audio_format = pyaudio.paInt16
channels = 1
rate = 40000

p = pyaudio.PyAudio()

playing_stream = p.open(format=audio_format, channels=channels, rate=rate, output=True,
                        frames_per_buffer=chunk_size)

recording_stream = p.open(format=audio_format, channels=channels, rate=rate, input=True,
                          frames_per_buffer=chunk_size)

connections = []

server_s = [socket.socket(socket.AF_INET, socket.SOCK_STREAM)]

print(socket.gethostname())
ip = "192.168.8.148"


def start_serv():
    def_port = 6000
    port = def_port

    server_s[0] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while 1:
        try:
            while True:
                try:
                    port = int(var_port.get())
                    break
                except ValueError:
                    print(bcolors.FAIL + "The entered port is invalid. Try again" + bcolors.ENDC)
                    var_port.set(def_port)

            server_s[0].bind((ip, port))

            var_server_status.set("Połączony")
            print(bcolors.WARNING + bcolors.UNDERLINE + f"Połączono\n" + bcolors.ENDC +
                  bcolors.BOLD + f"IP: {ip}\nPort: {port}" + bcolors.ENDC)

            break
        except:
            print(bcolors.FAIL + "Couldn't bind to that port. Searching for free port" + bcolors.ENDC)
            def_port = def_port + 1
            var_port.set(def_port)
            time.sleep(2)

            print(int(var_in_status.get()))

            if int(var_in_status.get()) == 0:
                print("in")
                break

    accept_connections(port)


def disconnect_server():
    try:
        server_s[0].close()
    except OSError:
        pass

    print(bcolors.FAIL + "Server disconnected" + bcolors.ENDC)
    var_connected_to.set("Not connected")
    var_in_status.set("0")


def accept_connections(port):
    server_s[0].listen(100)

    print(bcolors.OKGREEN + "Accepting new connections on:" + bcolors.ENDC)
    print(bcolors.BOLD + "IP: " + ip + bcolors.ENDC)
    print(bcolors.BOLD + "Port: " + str(port) + bcolors.ENDC)

    logging.info(1, var_server_status.get())

    while True:
        try:
            c, addr = server_s[0].accept()

            connections.append(c)

            var_connected_to.set(addr)

            threading.Thread(target=handle_client, args=(c, addr,)).start()
        except OSError:
            break


def talk(c, data):
    for client in connections:
        if client != server_s[0]:
            client.send(data)


def handle_client(c, addr):
    print(bcolors.OKBLUE + "Handling new connection" + bcolors.ENDC)

    def receive():
        while 1:
            data = c.recv(20000)
            # print(data[0])

            playing_stream.write(data)

            print("WRITED")
            print(data)

    def send():
        while 1:
            send_data = recording_stream.read(20000, exception_on_overflow=False)
            print("SENDED")
            time.sleep(0.01)
            talk(c, send_data)

    r_thread = threading.Thread(target=receive).start()
    s_thread = threading.Thread(target=send).start()
    # while 1:
    #     try:
    #
    #
    #     except socket.error as e:
    #         print("CLOSING")
    #         c.close()
    #         time.sleep(2)
    #         print(e)


########### CLIENT ###############


client_s = [socket.socket(socket.AF_INET, socket.SOCK_STREAM)]

client_p = pyaudio.PyAudio()

client_playing_stream = p.open(
    format=audio_format, channels=channels, rate=rate, output=True,
    frames_per_buffer=chunk_size
)

client_recording_stream = p.open(format=audio_format, channels=channels, rate=rate, input=True,
                                 frames_per_buffer=chunk_size)


def start_cli():
    client_s[0] = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    while 1:
        try:
            target_ip = var_ip.get()
            target_port = int(var_destinated_port.get())

            client_s[0].connect((target_ip, target_port))

            var_client_status.set("Client connected to " + target_ip)

            break
        except Exception as e:
            print(e)
            print("Couldn't connect to server")

    print(bcolors.OKBLUE + "Connection established" + bcolors.ENDC)

    # start threads
    receive_thread = threading.Thread(target=receive_server_data).start()
    send_thread = threading.Thread(target=send_data_to_server).start()


def disconnect_client():
    client_s[0].close()

    print(bcolors.FAIL + "Client disconnected" + bcolors.ENDC)


def receive_server_data():
    print("receiving")
    while True:
        try:
            # data = client_s[0].recv(1024)
            pass
            # playing_stream.write(data)
        except:
            pass


def send_data_to_server():
    print("sending")
    while True:
        try:
            pass
            # data = recording_stream.read(1024)
            # print("PRINTING BIANRY")
            # print(data[0])
            #
            # client_s[0].send(data)
        except:
            pass


def run_server():
    start_serv()


def run_client():
    start_cli()


def server_init():
    server_thread = threading.Thread(target=run_server).start()


def client_init():
    client_thread = threading.Thread(target=run_client).start()


def set_params():
    pass


def disconnect():
    disconnect_client()
    disconnect_server()


# TEXT
ip_label = ttk.Label(root, text="IP")
ip_label.grid(column=0, row=2)
# TEXT
port_label = ttk.Label(root, text="PORT")
port_label.grid(column=0, row=1)
# TEXT
dst_port_label = ttk.Label(root, text="DESTINATED PORT")
dst_port_label.grid(column=0, row=3)

# SERVER STATUS
status_lb = ttk.Entry(root, textvariable=var_server_status, state=DISABLED)
status_lb.grid(column=1, row=6)
status_label = ttk.Label(root, text="SERVER STATUS")
status_label.grid(column=0, row=6)

# CLIENT STATUS
status_lb = ttk.Entry(root, textvariable=var_client_status, state=DISABLED)
status_lb.grid(column=3, row=6, columnspan=5)
status_label = ttk.Label(root, text="CLIENT STATUS")
status_label.grid(column=2, row=6)

# Connection
connection_lb = ttk.Entry(root, textvariable=var_connected_to, state=DISABLED)
connection_lb.grid(column=1, row=7)
connection_label = ttk.Label(root, text="Server connected to: ")
connection_label.grid(column=0, row=7)

# Disconnect
disconnect_button = ttk.Button(root, text='Disconnect', command=disconnect)
disconnect_button.grid(column=2, row=5, sticky=(N, W, E, S), padx=10)

value = ttk.Entry(root, textvariable=var_ip)
value.grid(column=1, row=2, columnspan=4, sticky=(N, W, E, S))

value = ttk.Entry(root, textvariable=var_port)
value.grid(column=1, row=1, columnspan=4, sticky=(N, W, E, S))

value = ttk.Entry(root, textvariable=var_destinated_port)
value.grid(column=1, row=3, columnspan=4, sticky=(N, W, E, S))

# BUTTON START SERVER
edit_button = ttk.Button(root, text='Start server', command=server_init)
edit_button.grid(column=1, row=4, sticky=(N, W, E, S), padx=10)

# BUTTON START CLIENT
save_button = ttk.Button(root, text='Start connection', command=client_init)
save_button.grid(column=1, row=5, sticky=(N, W, E, S), padx=10)

# # BUTTON LOAD
# load_button = ttk.Button(root, text='LOAD', command=set_params)
# load_button.grid(column=1, row=6, sticky=(N,W,E,S), padx=10)

root.mainloop()
