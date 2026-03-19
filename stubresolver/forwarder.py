from socket import socket, timeout
import logging

def forward_query(parsed_packet: dict, data: bytes, upstream: tuple, upstream_sock: socket) -> tuple[bytes, int]:
    """Forward a DNS query to an upstream resolver and return the raw response bytes."""

    txn_id = parsed_packet["header"]["id"]
    upstream_sock.sendto(data, upstream)

    try:
        recursive_response, _ = upstream_sock.recvfrom(4096)
    except timeout:
        logging.error(f"[ERROR] Timeout receiving response from upstream")
        return b'', 0
    
    resp_id = int.from_bytes(recursive_response[:2], "big")
    if resp_id != txn_id:
        logging.warning(f"[WARNING] Transaction ID mismatch: expected {txn_id}, got {resp_id}")
        return b'', 0
    
    return recursive_response, resp_id
