import os
import socket
import sys
import threading


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# binding
server_address = ('localhost', 12000)
print >> sys.stderr, 'starting up on %s port %s' % server_address
sock.bind(server_address)

# listening
sock.listen(1)

curdir=['.']

def command(choice,koneksi_client):
    #option=choice.split()
    if(choice=='list'):
       # path='/'.join(curdir)
        files=os.listdir(".")
        message='\n'.join(files)
        koneksi_client.sendall(message.encode('utf-8'))
    # elif(option[0]=='chdir'):
    #     if len(option)<2:
    #         message="Perintah tidak dapat dilakukan"
    #         koneksi_client.sendall(message.encode('utf-8'))
    #     elif option[1]=='..':
    #         if len(curdir)>1:
    #             del curdir[-1]
    #         else:
    #             message="Perintah tidak dapat dilakukan"
    #             koneksi_client.sendall(message.encode('utf-8'))
    #     else:
    #         curdir.append(option[1])

    else:
        message="perintah tidak tersedia"
        koneksi_client.sendall(message.encode('utf-8'))

# main function for data processing
def layaniclient(koneksi_client, alamat_client):
    try:
        print >> sys.stderr, 'connection from ', alamat_client
        while True:
            message = koneksi_client.recv(64)
            if message:
                #print >> sys.stderr, 'received "%s"' % message
                command(message.decode('utf-8'),koneksi_client)
                #koneksi_client.sendall('returned from server: ' + message)
            else:
                break
    finally:
        koneksi_client.close()


while True:
    print >> sys.stderr, 'waiting for a connection'
    koneksi_client, alamat_client = sock.accept()
    # call the function using thread
    conn = threading.Thread(target=layaniclient, args=(koneksi_client, alamat_client))
    conn.start()


    # note: koneksi_client = socket