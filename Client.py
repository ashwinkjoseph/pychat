import socket
import json

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
#s.connect(('192.168.43.239', 8000));
s.connect(('localhost', 8000));
p = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
p.connect(('localhost', 8010));
print("client is running");
ret = []
while True:
    typ = input("id or name?")
    message = input("Enter the message");
    if(typ=="id"):
        smessage = {"intention":"search", "type":typ, "id":message}
    else:
        smessage = {"intention":"search", "type":typ, "name":message}
    smessage = json.dumps(smessage);
    if message!="quit":
        s.send(smessage.encode())
        while True:
            recieved = s.recv(3072);
            recieved = recieved.decode()
            if recieved == "1":
                s.close();
                break;
            if recieved == "error":
                print("Error");
                break;
            if recieved == "2":
                print("done")
                break;
            else:
                print(recieved)
                recieved = json.loads(recieved);
                ret.append({"id":recieved['emp_id'], "name":recieved['emp_name']});
                print("\n")
    else:
        s.send(message.encode())
        recieved = s.recv(3072);
        recieved = recieved.decode()
        if recieved == "1":
            s.close();
            break;
    break;
ch = []
n = int(input("Enter the number of items to be transferred"));
for i in range (n):
    ch.append(int(input("Enter the item to be transferred")));

smessage = {"intention":"add", "data":list()}
for c in ch:
    smessage['data'].append(ret[c]);

smessage = json.dumps(smessage);
p.send(smessage.encode());
recieved = p.recv(3072);
recieved = recieved.decode()
print(recieved)
if(recieved == "done"):
    message = {"intention":"delete", "data":list()}
    for c in ch:
        message['data'].append(ret[c]['id']);
    
    message = json.dumps(message);
    s.send(message.encode());
else:
    print("Failed");
while True:
    pass