def parse_query(data: bytes) -> dict:
    """Parse a raw DNS query packet and return structured query metadata."""

    # Header extraction - 12 bytes (As per 4.1 RFC 1035)
    header = {}
    header["id"] = int.from_bytes(data[:2], "big")
    temp = int.from_bytes(data[2:4], "big")
    header["qr"] = (temp >> 15) & 1
    header["Opcode"] = (temp >> 11) & 15
    header["aa"] = (temp >> 10) & 1
    header["tc"] = (temp >> 9) & 1
    header["rd"], header["ra"] = (temp >> 8) & 1, (temp >> 7) & 1
    header["z"] = (temp >> 4) & 7
    header["rcode"] = temp & 15
    header["qdcount"] = int.from_bytes(data[4:6], "big")
    header["ancount"] = int.from_bytes(data[6:8], "big")
    header["nscount"] = int.from_bytes(data[8:10], "big")
    header["arcount"] = int.from_bytes(data[10:12], "big")

    # Question Extraction (It's almost always qdcount=1)
    question = {}
    curr_pointer = 12
    while data[curr_pointer] != 0:
        curr_pointer += 1

    question["qname"] = extract_domain_name(data[12:curr_pointer])
    question["qtype"] = int.from_bytes(data[curr_pointer+1:curr_pointer+3], "big")
    question["qclass"] = int.from_bytes(data[curr_pointer+3: curr_pointer+5], "big")

    return {"header": header, "question": question}


def extract_domain_name(data: bytes) -> str:
    """Extract and decode the queried domain name from a DNS packet."""
    dname=""
    idx = 0
    curr_length = 0
    
    while idx < len(data) and data[idx] != 0 and not curr_length:
        curr_length = int(data[idx])
        dname += data[idx+1:idx+curr_length+1].decode('ascii') + '.'
        idx += curr_length+1
        curr_length = 0
        

    return dname[:-1]


# Query type extraction/parsing is not required for a stub resolver
# def extract_query_type(data: bytes) -> int:
#     """Extract the DNS record type requested in the incoming query."""
#     raise NotImplementedError("Implement query type extraction.")
