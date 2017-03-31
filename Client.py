import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
s.connect(('localhost', 8000));
print("client is running");
while True:
    message = input("Enter the message");
    s.send(message.encode());
    recieved = s.recv(1024);
    if recieved == b"1":
        s.close();
        break;
    else:
        print(recieved);