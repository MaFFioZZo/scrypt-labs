import socket


def start_udp_client(message='Hello, World!', host='127.0.0.1', port=57057):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        client_socket.sendto(message.encode(), (host, port))
        print(f'Message sent to {host}:{port}: {message}')
        
        data, addr = client_socket.recvfrom(1024)
        print(f'Server answer: {data.decode()}')

    finally:
        client_socket.close()
        print('Socket closed.')

def main():
    start_udp_client()

main()