import socket
import threading

def connection(conn, addr):
    print(str(addr)+"is now connected");
    while True:
        message = conn.recv(1024);
        print(message);
        if message == b"quit":
            conn.send("1".encode());
            break;
        else:
            conn.send(b"message recieved");

class threadit(threading.Thread):
    done = False;
    def setvalues(self, conn, addr, name):
        self.conn = conn;
        self.addr = addr;
        self.name = name;
    
    def getname(self):
        print(self.name);

    def run(self):
        connection(self.conn, self.addr);
        self.done = True;

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = '' ;
port = 8000;
s.bind((host, port));
s.listen(10);
print("Server is running");
conn = [];
addr = [];
connn = [];
i = 0;
while True:
    j = -1;
    for con in connn:
        j = j + 1;
        if con.done == True:
            del connn[j];
            i = i - 1;
    conn, addr = s.accept();
    connn.append(threadit(name = "connection"+str(i+1)));
    connn[i].setvalues(conn, addr, "connection"+str(i+1));
    connn[i].start();
    print("i="+str(i));
    for con in connn:
        con.getname();
    i = i+1;