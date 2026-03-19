import socket
from config import LISTEN_IP, LISTEN_PORT, TIMEOUT, UPSTREAM_DNS
from dns_parser import parse_query
from forwarder import forward_query
import logging
# from utils import log_request, log_response


def send_response(sock: socket.socket, response: bytes, client_address: tuple) -> None:
    """Send a DNS response packet back to the requesting client."""
    if not response:
        logging.warning(f"[WARNING] No response to send to {client_address}")
        return
    
    try:
        sock.sendto(response, client_address)
    except OSError as e:
        logging.error(f"[ERROR] Failed sending response to {client_address}: {e}")
    


def run_server() -> int:
    """Start the UDP socket loop and orchestrate parsing, forwarding, and response handling."""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_sock, \
         socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as upstream_sock:
        try:
            client_sock.bind((LISTEN_IP, LISTEN_PORT))
        except PermissionError:
            logging.error(
                f"[ERROR] Permission denied: Unable to bind to {LISTEN_IP}:{LISTEN_PORT}. Try running with elevated privileges or choose a different port."
            )
            return 2
        except OSError as e:
            logging.error(f"[ERROR] Bind failed on {LISTEN_IP}:{LISTEN_PORT}: {e}")
            return 2
        

        client_sock.settimeout(TIMEOUT)
        upstream_sock.settimeout(TIMEOUT)

        logging.info(f"DNS Stub Resolver running on {LISTEN_IP}:{LISTEN_PORT}, forwarding to {UPSTREAM_DNS[0]}:{UPSTREAM_DNS[1]}")

        try:
            while True:
                try:
                    data, client_address = client_sock.recvfrom(512)
                except socket.timeout:
                    continue  # No incoming query, just loop back and wait again
                except OSError as e:
                    logging.error(f"[ERROR] Error receiving data from client: {e}")
                    continue
                logging.info(f"IN QUERY from {client_address[0]}:{client_address[1]}")

                try:
                    query_info = parse_query(data)
                except Exception as e:
                    logging.error(f"[ERROR] Failed to parse query from {client_address}: {e}")
                    continue
                logging.info(f"UPSTREAM QUERY to {UPSTREAM_DNS[0]}:{UPSTREAM_DNS[1]}, txn_id:{query_info['header']['id']} - {query_info['question']['qname']}")

                try:
                    response, resp_id = forward_query(query_info, data, UPSTREAM_DNS, upstream_sock)
                except socket.timeout:
                    logging.error(f"[ERROR] Timeout forwarding query to upstream for {client_address}")
                    continue
                except Exception as e:
                    logging.error(f"[ERROR] Failed to forward query to upstream: {e}")
                    continue
                logging.info(f"UPSTREAM RESPONSE from {UPSTREAM_DNS[0]}:{UPSTREAM_DNS[1]}, txn_id:{resp_id}")

                try:
                    send_response(client_sock, response, client_address)
                except Exception as e:
                    continue
                logging.info(f"OUT RESPONSE to {client_address[0]}:{client_address[1]}, txn_id:{resp_id}")

        except KeyboardInterrupt:
            logging.info("Shutting down DNS Stub Resolver.")
            return 0
        except Exception as e:
            logging.error(f"[ERROR] An unexpected error occurred: {e}")
            return 1


if __name__ == "__main__":
    raise SystemExit(run_server())
