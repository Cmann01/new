import socket
import select
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

def receive():
    while True:
        try:
            message = client_socket.recv(2048).decode()
            chat_text.insert(tk.END, message + '\n')
        except:
            break

def send(event=None):
    message = my_message.get()
    my_message.set("")
    if message:
        formatted_message = "[{:%H:%M:%S}] Me: {}".format(datetime.now(), message)
        client_socket.send(message.encode())
        chat_text.insert(tk.END, formatted_message + '\n')

def create_room():
    room = simpledialog.askstring("Create Chat Room", "Enter room name:")
    if room:
        client_socket.send(room.encode())

def on_closing(event=None):
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        client_socket.close()
        window.quit()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("Server_IP_Address", Server_Port))

name = simpledialog.askstring("Name", "Enter your name:")
if not name:
    exit()
client_socket.send(name.encode())

room = simpledialog.askstring("Join Chat Room", "Enter room name:")
if not room:
    exit()
client_socket.send(room.encode())

window = tk.Tk()
window.title(f"Chat Room - {room}")

chat_text = tk.Text(window, height=20, width=60)
chat_text.pack()

my_message = tk.StringVar()
entry_field = tk.Entry(window, textvariable=my_message)
entry_field.bind("<Return>", send)
entry_field.pack()

send_button = tk.Button(window, text="Send", command=send)
send_button.pack()

create_room_button = tk.Button(window, text="Create Room", command=create_room)
create_room_button.pack()

window.protocol("WM_DELETE_WINDOW", on_closing)

receive_thread = threading.Thread(target=receive)
receive_thread.start()

tkinter.mainloop()
