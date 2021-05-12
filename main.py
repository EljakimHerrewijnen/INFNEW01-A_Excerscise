import sys
import json
import socket

student = "0912374: Eljakim Herrewijnen"

HS_PORT = 3002
S_PORT = 3001
S_HOST = "localhost"
HS_HOST = "localhost"
program_id = "[Client]"

def setupClient(book1):
    print(f"{program_id}Connecting to server on: {S_HOST}:{S_PORT}")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while(client.connect_ex((S_HOST, S_PORT)) != 0):
        pass
    print(f"{program_id}Connected! Sending intial hello message")
    message = {}
    message["Title"] = "Hello"
    message["Sender"] = "User1"
    client.send(json.dumps(message).encode('utf-8'))
    print(f"{program_id}Received: {client.recv(1024).decode('utf-8')}")

    #request book
    message = {}
    message["Title"] = "BookInquiry"
    message["BookName"] = book1
    client.send(json.dumps(message).encode('utf-8'))
    dat = client.recv(1024)
    if(dat != b''):
        book = json.loads(dat.decode('utf-8'))
        print(f"{program_id}Received: {book}")
        if(book['Status'] == ""):
            print("Book not found!")
        elif(book['Status'] == "Borrowed"):
            print(f"{program_id}Book is borrowed, Inquiring by user details...")
            message = {}
            message["Title"] = "UserInquiry"
            message["UserName"] = book['Borrowed by']
            client.send(json.dumps(message).encode('utf-8'))
            user = json.loads(client.recv(1024).decode('utf-8'))
            print(user)
        else:
            print(book)

    print(f"{program_id}Done. Sending Quit message to server and exiting")
    #Quit
    message = {}
    message["Title"] = "Quit"
    client.send(json.dumps(message).encode('utf-8'))
    client.close()



def setupServer():
    program_id = "[Server]"
    print(f"{program_id}Server starting. Connecting to Helper Server...")
    hs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while(hs.connect_ex((HS_HOST, HS_PORT)) != 0):
        pass
    print(f"{program_id}Hosting server on: {S_HOST}:{S_PORT}")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((S_HOST, S_PORT))
    server.listen(1) #only 1 connection needed
    conn, addr = server.accept()
    print(f"{program_id}Client1 has connected! {str(addr)} ")

    while(True):
        dat = conn.recv(1024)
        if(dat != b''):
            data = json.loads(dat.decode('utf-8'))
            print(f"{program_id}Received: {data}")
            #receive hello
            if(data["Title"] == "Hello"):
                #send welcome
                welcome = {}
                welcome["Title"] = "Hello"
                welcome["Content"]: "Welcome"
                conn.send(json.dumps(welcome).encode("utf-8"))
            elif(data["Title"] == "BookInquiry" or data["Title"] == "UserInquiry"):
                print(f"{program_id}Inquiring: {data}")
                hs.send(dat)
                conn.send(hs.recv(1024))
            elif(data["Title"] == "Quit"):
                q = {}
                q['Title'] = "Quit"
                hs.send(json.dumps(q).encode('utf-8'))
                conn.close()
                server.close()
                hs.close()
                return
        else:
            pass

    


def setupHelperServer(users, books):
    program_id = "[HelperServer]"
    print(f"{program_id}Hosting server on: {HS_HOST}:{HS_PORT}")
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Tell the socket to be reused if closed unexpectedly
    server.bind((HS_HOST, HS_PORT))
    server.listen(1) #only 1 connection needed
    conn, addr = server.accept()
    print(f"{program_id}Server has connected! ip,port: {str(addr)}")
    while(True):
        dat = conn.recv(1024)
        if(dat != b''):
            data = json.loads(dat.decode('utf-8'))
            print(f"{program_id}Received: {data}")
            if(data["Title"] == "BookInquiry"):
                print(f"{program_id}Searching for: {data['BookName']}")
                found = False
                for x in books:
                    if(x['Book title'] == data['BookName']):
                        conn.send(json.dumps(x).encode('utf-8'))
                        found = True
                if(not found):
                    notfound = x
                    notfound["Status"] = ""
                    conn.send(json.dumps(notfound).encode("utf-8"))
            elif(data["Title"] == "UserInquiry"):
                print(f"{program_id}Searching for: {data['UserName']}")
                found = False
                for x in users:
                    if(x['Name'] == data['UserName']):
                        conn.send(json.dumps(x).encode('utf-8'))
                        found = True
                if(not found):
                    notfound = x
                    notfound["Name"] = ""
                    conn.send(json.dumps(notfound).encode("utf-8"))
            elif(data["Title"] == "Quit"):
                conn.close()
                server.close()
                return
        else:
            pass

def printHelp():
    print("Networking retake assignment:")
    print(student)
    print("This script runs in 3 different modes: Client(C) or Server(S) or Helper Server(HS):")
    print("Usage:")
    print("Client:")
    print("\t main.py C Optional: <ipaddress/host to server>:<port>")
    print("\t Connects by default to localhost:3001")
    print("Server:")
    print("\t main.py S Optional: <ipaddress/host to helper server>:<port> Optional: <ipaddress/host NIC to run from>:<port>")
    print("\t Server runs by default on port 3001")
    print("Helper Server:")
    print("\t main.py HS users.json books.json Optional: <ipaddress/host NIC to run from>:<port>")
    print("\t Server runs by default on port 3002")

def main():
    if(len(sys.argv) < 2):
        printHelp()
        print("You need to specify a program mode!")
        return
    if(sys.argv[1] == "C"):
        if(len(sys.argv) == 4):
            S_HOST = sys.argv[3].split(':')[0]
            S_PORT = sys.argv[3].split(':')[1]
        setupClient(sys.argv[2])
    elif(sys.argv[1] == "S"):
        if(len(sys.argv) == 3):
            HS_HOST = sys.argv[3].split(':')[0]
            HS_PORT = sys.argv[3].split(':')[1]
        elif(len(sys.argv) == 4):
            HS_HOST = sys.argv[3].split(':')[0]
            HS_PORT = sys.argv[3].split(':')[1]
            S_HOST = sys.argv[4].split(':')[0]
            S_PORT = sys.argv[4].split(':')[1]
        setupServer()
    elif(sys.argv[1] == "HS"):
        if(len(sys.argv) < 4):
            printHelp()
        else:
            users = json.load(open(sys.argv[2], "r"))
            books = json.load(open(sys.argv[3], "r"))
            if(len(sys.argv) == 5):
                HS_HOST = sys.argv[4].split(':')[0]
                HS_PORT = sys.argv[4].split(':')[1]
            setupHelperServer(users, books)
    else:
        printHelp()

if __name__ == "__main__":
    main()