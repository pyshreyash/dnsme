"""Utility placeholders for resolver logging and shared helpers."""


def log_request(client_address: tuple, query_info: dict) -> None:
    """Record incoming DNS request details for observability and debugging."""
    pass


def log_response(client_address: tuple, response_size: int) -> None:
    """Record outbound DNS response details for observability and debugging."""
    pass
