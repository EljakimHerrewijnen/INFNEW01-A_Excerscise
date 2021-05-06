import sys
import socket
import json

Student_name = "Eljakim Herrewijnen"
Student_number = "0912374"

HOST= '145.24.222.133'
PORT = 55550
ID = 1

client1 = None
client1_shared = None
c1_c2_conn = None
client2 = None
client2_shared = None
c2_server = None

data = {
    "studentnr1": "Your_studentnumber",
    "studentnr2": "The student number of your teammate",
    "classname": "YOURCLASSCODE",
    "clientid": "-1",
    "teamname": "YOUR TEAM NAME SHOULD BE HERE",
    "ip": "YOUROWNIPADDRESS",
    "secret": "",
    "status": ""
}

def ClientPrint(id, msg):
    print("[Client{}] {}".format(id, msg))

def GetMessage(id1, id2, classcode, clientid, teamname, ip, secret, status):
    t = data
    t['studentnr1'] = id1
    t['studentnr2'] = id2
    t['classname'] = classcode
    t['clientid'] = clientid
    t['teamname'] = teamname
    t['ip'] = ip
    t['secret'] = secret
    t['status'] = status
    return t

def SetupSocket(id):
    print("[Client{}] Establishing connection".format(id))
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))
    return sock

def Client1(host, port):
    print("Client2 {}:{}".format(host, port))
    c1_c2_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Connecting to Client2. Make sure Client2 is up and running")
    # while(c1_c2_conn.connect_ex((host, port)) != 0):
    #     pass

    ClientPrint(1, "Connected to Client2")
    client1 = SetupSocket(1)
    r1 = client1.recv(1024).decode('utf-8')
    ClientPrint(1, "Connected. Message from server: " + r1)
    ClientPrint(1, "Sending our data without secret to server")
    dat1 = json.dumps(GetMessage('0912374', '0000000', 'RETAKE', ID, 'Eljakim', '192.168.1.1', "", "")).encode('utf-8')
    client1.send(dat1)
    dat = client1.recv(1024)
    ClientPrint(1, "Received data from server. Sending it via socket to Client2")
    c1_c2_conn.send(dat)
    ClientPrint(1, "Closing client1 socket")
    client1.close()

def Client2(host, port):
    ClientPrint(2, "Setting up a server socket to accept connections from client1 ({}:{})".format(host, port))
    c2_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    c2_server.bind((host, 55551))
    c2_server.listen(1) #only 1 connection needed
    conn, addr = c2_server.accept()
    ClientPrint(2, "Client1 has connected! ip,port: " + str(addr))
    ClientPrint(2, "Waiting for message from client1")
    client2_shared = json.loads(conn.recv(1024).decode('utf-8'))
    ClientPrint(2, "Received data from client1. status: " + client2_shared['status'])

    #Connect to server
    client2 = SetupSocket(2)
    r2 = client2.recv(1024).decode('utf-8')
    ClientPrint(2, "Connected. Message from server: " + r2)

    #alter data to our own
    temp = client2_shared['studentnr2']
    client2_shared['studentnr2'] = client2_shared['studentnr1']
    client2_shared['studentnr1'] = temp
    client2_shared['clientid'] = 2
    client2_shared['ip'] = host
    ClientPrint(2, "Done, sending data to server")
    client2.send(json.dumps(client2_shared).encode('utf-8'))
    r2 = json.loads(client2.recv(1024).decode('utf-8'))
    ClientPrint(2, "Server responded with: " + str(r2))
    client2.close()



# def Automatic():
#     print("Automated testing. We setup 2 sockets to the target server({}:{}).\nClient2 deploys a socket server and client1 connects to this server.\nIP address for the server is just localhost, with port 55551".format(HOST, PORT))
#     thread1 = threading.Thread(target=Client1, args=(socket.gethostname(), 55551, ))
#     thread2 = threading.Thread(target=Client2, args=(socket.gethostname(), 55551, ))
#     thread2.start()
#     thread1.start()
#     thread1.join()
#     thread2.join()

def printHelp():
    print("Example usage:")
    print("You need 2 clients for this excercise. Run them as follows:")
    print("Client1: python main.py 1")
    print("Client2: python main.py 2")

if __name__== "__main__":
    printHelp()
    if(len(sys.argv) > 1):
        if(sys.argv[1] == "1" or sys.argv[1] == "client1"):
            print("Running as client 1. You need to open a second client to connect to this one")
            Client1(socket.gethostname(), 55551)
        elif(sys.argv[1] == "2" or sys.argv[1] == "client2"):
            print("Running as client 2, connecting to client 1")
            Client2(socket.gethostname(), 55551)
        else:
            printHelp()
    else:
        printHelp()
        #parse arguments
    

