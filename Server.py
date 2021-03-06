import socket
import threading
import MySQLdb as mdb   
import json

f = open("server_config.json", 'r');
obj = f.read();
f.close();
obj = json.loads(obj)

db_conn = mdb.connect(host=obj['db_server'], user=obj['user'], passwd=obj['password'], db=obj['database'])
with db_conn:
    class database:
        def __init__(self):
            self.cur = db_conn.cursor(mdb.cursors.DictCursor);
            self.stat = False;

        def fetch(self, cur):
            for i in range(cur.rowcount):
                row = self.cur.fetchone();
                return row;

        def retrieve(self, id=-1, name="none"):
            if name!="none":
                if id!=-1:
                    self.cur.execute("SELECT * FROM employee WHERE (emp_name LIKE %s) AND (emp_id = "+str(id)+")", ("%"+str(name)+"%",))
                    self.rows = self.cur.fetchall();
                    self.stat = True;
                else:
                    st = str("%"+str(name)+"%")
                    self.cur.execute("SELECT * FROM employee WHERE emp_name LIKE %s", (st,))
                    self.rows = self.cur.fetchall();
                    self.stat = True;
            else:
                if id!=-1:
                    self.cur.execute("SELECT * FROM employee WHERE emp_id = "+str(id))
                    self.rows = self.cur.fetchall();
                    self.stat = True;
                else:
                    self.stat = False;

        def send(self, id, name):
            if(self.cur.execute("INSERT INTO employee VALUES(emp_id, %s)", (str(name),))):
                return True
            else:
                return False

        def remv(self, data):
            if(self.cur.execute("DELETE FROM employee WHERE emp_id=%s",(str(data),))):
                return True
            else:
                return False

        def logit(self, data):
            f = open("log.json", "w+");
            data = json.dumps(data)
            if(f.write(data)):
                stat = True
            else:
                stat = False
            f.write("\n")
            f.close()
            return stat

    def connection(conn, addr):
        print(str(addr)+"is now connected");
        req = database();
        while True:
            message = conn.recv(1024);

            if message == b"quit":
                conn.send("1".encode());
                break;

            message = message.decode();
            print(message);
            r = json.loads(message);
            if(r['intention']=="search"):
                if(r['type']=="id"):
                    req.retrieve(id=int(r['id']));
                else:
                    req.retrieve(name=r['name'])
                if req.stat:
                    for rowi in req.rows:
                        rowi = json.dumps(rowi);
                        print("\n")
                        conn.send(rowi.encode())
                        print (rowi);
                        print("\n")
                    conn.send("2".encode());
                else:
                    conn.send("error".encode());
            elif(r['intention']=="add"):
                stat = int()
                for data in r['data']:
                   print(data)
                   stat = req.send(int(data['id']), data['name']);
                if(stat==True):
                    conn.send("done".encode())
                else:
                    conn.send("error".encode())
                break;
            elif(r['intention']=="delete"):
                stat = int()
                for data in r['data']:
                    print(data)
                    if(req.logit(data)):
                        stat = req.remv(int(data['id']))
                    else:
                        print("Logging Failed");
                        stat = False
                if(stat==True):
                    conn.send("done".encode())
                else:
                    conn.send("error".encode())
                break;
            else:
                conn.send("Program Error".encode());
                break;

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
    print("Server1 is running");
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