import ipaddress
import re

def validate_ip(ip_str):
    """
    Validates if a string is a valid IPv4 address.
    Returns True if valid, False otherwise.
    """
    try:
        ipaddress.IPv4Address(ip_str)
        return True
    except ipaddress.AddressValueError:
        return False

def validate_zone(zone_name):
    """
    Validates if a zone name is strictly alphanumeric and safe for chains.
    Returns True if valid, False otherwise.
    """
    if not zone_name:
        return True # Default zone is None/Empty which is handled as INPUT
    return bool(re.match(r'^[a-zA-Z0-9]+$', zone_name))

def validate_protocol(protocol):
    """Validates if a protocol is supported."""
    return protocol.lower() in ['tcp', 'udp', 'icmp', 'all']

def validate_interface(iface):
    """
    Validates if a network interface name is strictly alphanumeric plus dots and dashes.
    """
    if not iface:
        return True
    return bool(re.match(r'^[a-zA-Z0-9\.\-]+$', iface))

def sanitize_port(port):
    """
    Ensures port or port range is within valid range (1-65535).
    Example valid: "80", 80, "80:90"
    Returns str (to accommodate ranges) if valid, None otherwise.
    """
    if isinstance(port, int):
        if 1 <= port <= 65535:
            return str(port)
        return None
    
    port_str = str(port).strip()
    
    # Handle range
    if ':' in port_str or '-' in port_str:
        separator = ':' if ':' in port_str else '-'
        parts = port_str.split(separator)
        if len(parts) == 2:
            try:
                start = int(parts[0])
                end = int(parts[1])
                if 1 <= start <= 65535 and 1 <= end <= 65535 and start <= end:
                    return f"{start}:{end}"
            except ValueError:
                pass
        return None

    # Handle single port
    try:
        p = int(port_str)
        if 1 <= p <= 65535:
            return str(p)
    except ValueError:
        pass
    return None
