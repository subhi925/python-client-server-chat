import socket
import time  
from threading import Thread
from tkinter import *


# ------Encrypt-----------
def enc(my_message, distance):
    cipher_text = ""
    if distance > 26:
        distance %= 26
    for ch in my_message:
        if "a" <= ch <= "z":
            data = ord(ch) + distance
            if data > ord("z"):
                data -= 26
            cipher_text += chr(data)
        elif "A" <= ch <= "Z":
            data = ord(ch) + distance
            if data > ord("Z"):
                data -= 26
            cipher_text += chr(data)
        else:
            cipher_text += ch
    return cipher_text


# ------SendingClass------
class SendingThread(Thread):

    def __init__(self, mySocket, sendMsg):  
        Thread.__init__(self)  
        self.mySocket = mySocket
        self.sendMsg = sendMsg

    def run(self):  
        data = self.sendMsg
        self.mySocket.send(bytes(data, "utf-8"))


# ------ReceiveClass--------
class ReceivingThread(Thread):

    def __init__(self, mySocket, update_message): 
        Thread.__init__(self)  
        self.mySocket = mySocket
        self.update_message = update_message

    def run(self):  
        while True:
            try:
                msg = self.mySocket.recv(1024)
                if not msg:
                    break
                dec_msg = msg.decode("utf-8")
                self.update_message(dec_msg)
            except:
                break


# -------TinkerClasss----
class ChatBox:

    def __init__(self, master, mySocket):
        self.inputField = StringVar()
        self.message = StringVar()
        self.mySocket = mySocket  

        self.frame = Frame(master)
        self.frame.pack()

        Label(
            self.frame, text="Ask server for help", font=("Arial", 16), bg="red"
        ).pack(fill=X)

 
        self.chatBox = Label(
            self.frame,
            textvariable=self.message,
            bg="white",
            font=("Arial", 14),
            width=40,
            height=10,
            justify=LEFT,
            anchor="nw",
        )
        self.chatBox.pack(side=TOP, fill=X)

        self.messageEntry = Entry(
            self.frame, textvariable=self.inputField, font=("Arial", 12)
        ).pack(fill=X)
        self.senBtn = Button(
            self.frame, text="send", command=self.sendmsg
        ).pack(fill=X)

       
        self.message.set("[Chat Log]\n---------------------")

    def sendmsg(self):
        dis = 3  
        raw_text = self.inputField.get()
        encrypted_msg = enc(raw_text, dis)


        self.mySocket.send(bytes(str(dis), "utf-8"))
        time.sleep(0.1)  


        sendThread = SendingThread(self.mySocket, encrypted_msg)
        sendThread.start()


        formatted_ui = (
            f"[Chat Log]\n"
            f"---------------------\n"
            f'You (Client): "{raw_text}"\n\n'
            f"[Message sent successfully]\n"
            f"---------------------"
        )
        self.message.set(formatted_ui)
        self.inputField.set("")

    def update_message(self, new_msg):
        self.message.set(new_msg)


# ------Socket Setup------
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("127.0.0.1", 2010))  # Sending a connection request to the server

# ---------TK------
window = Tk()
window.title("ChatBox")
window.geometry("800x600")
window.configure(bg="lightblue")

chatbox = ChatBox(window, s)

receiveThread = ReceivingThread(s, chatbox.update_message)
receiveThread.start()

# Start Tkinter main loop
window.mainloop()
