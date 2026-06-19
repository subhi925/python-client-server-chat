import socket
from threading import Thread


def dec(my_message, distance):
    dec_text = ""
    if distance > 26:
        distance %= 26
    for ch in my_message:
        if "a" <= ch <= "z":
            data = ord(ch) - distance
            if data < ord("a"):
                data += 26
            dec_text += chr(data)
        elif "A" <= ch <= "Z":
            data = ord(ch) - distance
            if data < ord("A"):
                data += 26
            dec_text += chr(data)
        else:
            dec_text += ch
    return dec_text


class SendingThread(Thread):

    def __init__(self, mySocket):
        Thread.__init__(self)  
        self.mySocket = mySocket

    def run(self):  # Thread task
        while True:
            try:
                data = input()
                self.mySocket.send(bytes(data, "utf-8"))
            except:
                break


class ReceivingThread(Thread):

    def __init__(self, mySocket):
        Thread.__init__(self)  
        self.mySocket = mySocket

    def run(self):  
        while True:
            try:
                
                dis_data = self.mySocket.recv(1024).decode("utf-8")
                if not dis_data:
                    break

                dis = int(dis_data)

                
                enc_msg = self.mySocket.recv(1024).decode("utf-8")
                dec_msg = dec(enc_msg, dis)

                
                print(f"Encrypted: {enc_msg}")
                print(f"Decrypted: {dec_msg}")

            except Exception as e:
                break


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
s.bind(("127.0.0.1", 2010))
s.listen()

print("Server")  
mySocket, address = s.accept()


print(f"Connected: {address[0]}")

sendThread = SendingThread(mySocket)
receiveThread = ReceivingThread(mySocket)
sendThread.start()
receiveThread.start()
