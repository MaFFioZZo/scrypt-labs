import socket


def start_tcp_client(message='Hello, World!', host='127.0.0.1', port=56056):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((host, port))
        print(f'Connected to server {host}:{port}')

        client_socket.sendall(message.encode())
        print(f'Message sent: {message}')

        data = client_socket.recv(1024)
        print(f'Server answer: {data.decode()}')

    finally:
        client_socket.close()
        print('Connection closed.')


def main():
    start_tcp_client('Hello, World!')
   
main();