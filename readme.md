<h1>Networking assignment by Eljakim Herrewijnen</h1>
<p>
<b>Student1:</b> 0912374

<b>Student2:</b> -

</p>
</br>
<h2>Usage</h2>
I used the following libraries

socket, threading, json, argparse, time

> python3 main.py [-h] [--host HOST] [--port PORT] [--h2 H2] [--p2 P2] mode

</br>
The program can be run in different modes:
<li><b>client1 or 1:</b> Run as client1. This requires Client2 to be running already because Client2 initiates a socket server to which client1 connects</li>
<li><b>client2 or 2:</b> Run as client2. </li>
<li><b>client1 or 1:</b> Run automated. This creates 2 threads, client1 and client2. Both threads connect to the server. Client2 thread creates a socket server, to which client1 connects. After client1 has received data from the server it sends this data to client2 which than completes the request</li>

</br>
<b>When using 2 computers, make sure the port is opened in your firewall</b>

</br>
<h3>Example Usages: </h3>

> python3 main.py automated

```shell
$ python3 main.py automated
Automated testing. We setup 2 sockets to the target server(145.24.222.133:55550).
Client2 deploys a socket server and client1 connects to this server.
IP address for the server is just localhost, with port 55551
[Client2] Setting up a server socket to accept connections from client1 (Asusz87a-4790K:55551)
Client2 Asusz87a-4790K:55551
[Client1] Connected to Client2
[Client2] Client1 has connected! ip,port: ('127.0.0.1', 33562)
[Client1] Establishing connection
[Client2] Waiting for message from client1
[Client1] Connected. Message from server: Great! You managed to establish a socket connection to the server!'.

[Client1] Sending our data without secret to server
[Client1] Received data from server. Sending it via socket to Client2
[Client2] Received data from client1. status: waiting for message 2
[Client1] Closing client1 socket
[Client2] Establishing connection
[Client2] Connected. Message from server: Great! You managed to establish a socket connection to the server!'.

[Client2] Done, sending data to server
[Client2] Server responded with: {'studentnr1': '0000000', 'studentnr2': '0912374', 'classname': 'RETAKE', 'clientid': 2, 'teamname': 'Eljakim', 'ip': 'Asusz87a-4790K', 'secret': 'f3e5cacf1bf87d545859c49d90ee3c52baac5bd3baf0858f2718000c8a3c79f9', 'status': 'Finished successfully'}

```

> python3 main.py 2 --h2 '192.168.4.150' --p2 55551                                            

```
shell$ python3 main.py 2 --h2 '192.168.4.150' --p2 55551                                            
[Client2] Setting up a server socket to accept connections from client1 (192.168.4.150:55551)
[Client2] Client1 has connected! ip,port: ('192.168.4.19', 44166)
[Client2] Waiting for message from client1                                                     
[Client2] Received data from client1. status: waiting for message 2                            
[Client2] Establishing connection
[Client2] Connected. Message from server: Great! You managed to establish a socket connection to the server!'.

[Client2] Done, sending data to server                                                         
[Client2] Server responded with: {'studentnr1': '0000000', 'studentnr2': '0912374', 'classname': 'RETAKE', 'clientid': 2, 'teamname': 'Eljakim', 'ip': '192.168.4.150', 'secret': 'f3e5cacf1bf
87d545859c49d90ee3c52baac5bd3baf0858f2718000c8a3c79f9', 'status': 'Finished successfully'}
Running as client2
```


> python3 main.py 1 --h2 '192.168.4.150' --p2 55551

``` shell
$ python3 main.py 1 --h2 '192.168.4.150' --p2 55551
Client2 192.168.4.150:55551
[Client1] Connected to Client2
[Client1] Establishing connection
[Client1] Connected. Message from server: Great! You managed to establish a socket connection to the server!'.

[Client1] Sending our data without secret to server
[Client1] Received data from server. Sending it via socket to Client2
[Client1] Closing client1 socket
Running as client1

```

> python3 main.py student

```shell
$ python3 main.py student
Student_name: Eljakim Herrewijnen
Student_number0912374
```
