import socket

from config import LISTEN_IP, LISTEN_PORT, TIMEOUT, UPSTREAM_DNS
from dns_parser import parse_query
from forwarder import forward_query
from utils import log_request, log_response


def send_response(sock: socket.socket, response: bytes, client_address: tuple) -> None:
    """Send a DNS response packet back to the requesting client."""
    raise NotImplementedError("Implement response transmission to client.")


def run_server() -> None:
    """Start the UDP socket loop and orchestrate parsing, forwarding, and response handling."""
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((LISTEN_IP, LISTEN_PORT))
        # sock.settimeout(TIMEOUT)

        while True:
            data, client_address = sock.recvfrom(512)
            query_info = parse_query(data)
            exit(1)
            log_request(client_address, query_info)
            response = forward_query(data, UPSTREAM_DNS)
            send_response(sock, response, client_address)
            log_response(client_address, len(response))


if __name__ == "__main__":
    run_server()
