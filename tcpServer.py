import socket
import sys
import yaml
from datetime import date
from datetime import datetime
import time
import subprocess
import logging
import os


with open(os.path.dirname(os.path.realpath(__file__)) + "\config.yaml", 'r') as stream:
    try:
        config = yaml.safe_load(stream)
        
        print(config['commands'].values())
        print(config['commands'].keys())
    except yaml.YAMLError as exc:
        print(exc)

# Global params
login = False
attempts = 0
logging.basicConfig(filename='C:\\tcpServer\\server.log', level=logging.DEBUG)

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = (config['bind'], config['port'])
print('starting up on {} port {}'.format(*server_address))
logging.debug('starting up on {} port {}'.format(*server_address))

sock.bind(server_address)

# Listen for one incoming connection
sock.listen(1)



while True:
    # Wait for a connection
    print('waiting for a connection')
    logging.debug('%s: waiting for a connection',datetime.now())
    connection, client_address = sock.accept()
    connection.settimeout(config['timeout'])

    try:
        today = date.today()
        print('connection from', client_address)
        logging.debug('%s: connection from: %s', datetime.now(), client_address)
        today = today.strftime("%d.%m.%Y")
        logging.debug('date:  %s', today)
        connection.sendall(config['welcome_Message'].encode('utf-8'))
        
        # please login
        connection.sendall((str("Login Token:")).encode('utf-8'))
       
        # Receive the data in small chunks and retransmit it
        while True:
            data = connection.recv(config['buffer_size'])

            if data:
                msg = data.decode('utf-8').replace("\n", "")
                print('incoming msg:' , msg)
                logging.debug('%s: incoming command: %s',datetime.now(), msg)

                # check if logged in
                if login:
                    if msg == 'help':
                        connection.sendall((str("#### implemented commands ####" + "\n")).encode('utf-8'))
                        for cmd in config['commands'].keys():
                            connection.sendall((str(cmd + "\n")).encode('utf-8'))

                    elif msg == 'close':
                        login = False
                        connection.close()
                        break

                    elif msg in config['commands']:
                        command = config['commands'][msg]['call'] 
                        args = config['commands'][msg]['arg'].split(', ')                 
                        result = subprocess.run([command] + args, stdout=subprocess.PIPE)                       
                        connection.sendall(result.stdout)

                    else:
                        connection.sendall((str("#### unknown command, pls use help ####" + "\n")).encode('utf-8'))

                else:
                    # Login section
                    
                    # Bruteforce protection
                    if attempts > 2:
                        connection.sendall((str("To many failed login attempts, please wait")).encode('utf-8'))
                        logging.debug('%s: To many failed login attempts', datetime.now())
                        time.sleep(30)
                        attempts = 0                   

                    if msg == today:
                        connection.sendall((str("#### login sucessfull ####" + "\n")).encode('utf-8'))
                        login = True
                    else:
                        connection.sendall((str("#### login failed ####" + "\n")).encode('utf-8'))
                        attempts += 1
                        connection.sendall((str("Login Token:")).encode('utf-8'))
            
                connection.sendall((str("\n" + ">>")).encode('utf-8'))
                
            else:
                print('no data from', client_address)
                break

    except socket.timeout:
        print('client timeout, connection closed')
        logging.debug('client timeout, connection closed')

    finally:
        # Clean up the connection
        connection.close()