import socket


def start_tcp_server(host='127.0.0.1', port=56056):
    server_socket = socket.socket(socket.AF_INET)
    server_socket.bind((host, port))

    server_socket.listen(1)
    print(f'TCP server {host}:{port} started. Waiting for connection...')

    conn, addr = server_socket.accept()
    print(f'Connected: {addr}')

    while True:
        data = conn.recv(1024)
        print(f'Recieved message: {data.decode()}')

        conn.sendall(data)
        print('Message resent')

        conn.close()
        server_socket.close()
        print(f'TCP server {host}:{port} stopped.')
        
        break;


def main():
    start_tcp_server()

main();