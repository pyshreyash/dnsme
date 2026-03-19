"""DNS upstream forwarding placeholders."""
from socket import socket

def forward_query(parsed_packet: dict, data: bytes, upstream: tuple, upstream_sock: socket) -> bytes:
    """Forward a DNS query to an upstream resolver and return the raw response bytes."""
    upstream_sock.settimeout(0.5)

    txn_id = parsed_packet["id"]
    upstream_sock.sendto(data, upstream)

    try:
        recursive_response, _ = upstream_sock.recvfrom(4096)
    except TimeoutError as e:
        print(f"Error receiving response from upstream: {e}")
        return b''
    
    resp_id = int.from_bytes(recursive_response[:2], "big")
    if resp_id != txn_id:
        print(f"Transaction ID mismatch: expected {txn_id}, got {resp_id}")
        return b''
    
    return recursive_response
