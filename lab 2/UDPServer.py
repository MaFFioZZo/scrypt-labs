import socket


def start_udp_server(host='127.0.0.1', port=57057):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((host, port))
    
    print(f'UDP server {host}:{port} started. Waiting for connection...')

    while True:
        data, addr = server_socket.recvfrom(1024)
        print(f'Recieved message from {addr}: {data.decode()}')
        
        server_socket.sendto(data, addr)
        print('Message resent')
        
        server_socket.close()
        print(f'UDP Server {host}:{port} stopped.')
        
        break;

def main():
    start_udp_server()

main();