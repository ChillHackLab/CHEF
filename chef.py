#!/usr/bin/env python3
from boofuzz import *
import logging
import sys
# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)
# Supported protocols and ports
ports = {
    80: "HTTP",
    443: "HTTPS",
    8080: "HTTP-ALT",
    8443: "HTTPS-ALT",
    21: "FTP",
    25: "SMTP",
    110: "POP3",
    143: "IMAP",
    23: "Telnet",
    53: "DNS",
    161: "SNMP",
    502: "Modbus",
    554: "RTSP",
    5060: "SIP",
    445: "SMB",
    3389: "RDP",
    1883: "MQTT",
    69: "TFTP",
    67: "DHCP",
    68: "DHCP",
    830: "NETCONF"
}
# UDP ports
udp_ports = [53, 161, 69, 67, 68, 5060] # DNS, SNMP, TFTP, DHCP, SIP
def define_protocol(session, port, proto_name):
    """Define protocol blocks for aggressive fuzzing"""
    s_initialize(f"{proto_name}_request")
   
    if proto_name in ["HTTP", "HTTPS", "HTTP-ALT", "HTTPS-ALT"]:
        s_string("GET", fuzzable=True)
        s_delim(" ")
        s_string("/fuzz", fuzzable=True, max_len=20000)
        s_string(" HTTP/1.1\r\n")
        s_string("Host: ")
        s_string("target.com", fuzzable=True, max_len=20000)
        s_string("\r\nUser-Agent: ")
        s_string("Mozilla/5.0", fuzzable=True, max_len=20000)
        s_string("\r\nContent-Length: ")
        s_int(1000, fuzzable=True)
        s_string("\r\n\r\n")
        s_bytes(b"A" * 20000, fuzzable=True) # Reduced buffer
    elif proto_name == "FTP":
        s_string("USER ", fuzzable=False)
        s_string("anonymous", fuzzable=True, max_len=20000)
        s_string("\r\n")
        s_string("PASS ", fuzzable=False)
        s_string("fuzz@fuzz.com", fuzzable=True, max_len=20000)
        s_string("\r\n")
    elif proto_name in ["SMTP", "SMTPS", "SMTP-SUBMISSION"]:
        s_string("HELO ", fuzzable=False)
        s_string("fuzz.com", fuzzable=True, max_len=20000)
        s_string("\r\n")
        s_string("MAIL FROM: ")
        s_string("fuzz@fuzz.com", fuzzable=True, max_len=20000)
        s_string("\r\n")
        s_string("RCPT TO: ")
        s_string("target@target.com", fuzzable=True, max_len=20000)
        s_string("\r\nDATA\r\n")
        s_bytes(b"A" * 20000, fuzzable=True)
        s_string("\r\n.\r\n")
    elif proto_name in ["POP3", "IMAP"]:
        s_string("a1 LOGIN ", fuzzable=False)
        s_string("fuzzuser", fuzzable=True, max_len=20000)
        s_string(" ")
        s_string("fuzzpass", fuzzable=True, max_len=20000)
        s_string("\r\n")
        s_bytes(b"A" * 20000, fuzzable=True)
    elif proto_name == "Telnet":
        s_string("login: ", fuzzable=False)
        s_string("fuzzuser", fuzzable=True, max_len=20000)
        s_string("\r\n")
        s_string("password: ", fuzzable=False)
        s_string("fuzzpass", fuzzable=True, max_len=20000)
        s_string("\r\n")
    elif proto_name == "DNS":
        s_bytes(b"\xAA\xAA", fuzzable=True)
        s_bytes(b"\x01\x00", fuzzable=True)
        s_string("fuzz.com", fuzzable=True, max_len=20000)
    elif proto_name == "SNMP":
        s_bytes(b"\x30\x82\x02\x00", fuzzable=True)
        s_string("public", fuzzable=True, max_len=20000)
    elif proto_name == "Modbus":
        s_bytes(b"\x00\x01", fuzzable=True)
        s_int(1, fuzzable=True)
        s_bytes(b"A" * 20000, fuzzable=True)
    elif proto_name == "RTSP":
        s_string("DESCRIBE ", fuzzable=True)
        s_string("rtsp://fuzz.com", fuzzable=True, max_len=20000)
        s_string(" RTSP/1.0\r\n")
        s_bytes(b"A" * 20000, fuzzable=True)
    elif proto_name == "SIP":
        s_string("INVITE sip:", fuzzable=True)
        s_string("fuzz@target.com", fuzzable=True, max_len=20000)
        s_string(" SIP/2.0\r\n")
        s_bytes(b"A" * 20000, fuzzable=True)
    elif proto_name == "SMB":
        s_bytes(b"\xFF\x53\x4D\x42", fuzzable=True)
        s_bytes(b"A" * 20000, fuzzable=True)
    elif proto_name == "RDP":
        s_bytes(b"\x03\x00", fuzzable=True)
        s_bytes(b"A" * 20000, fuzzable=True)
    elif proto_name == "MQTT":
        s_bytes(b"\x10", fuzzable=True)
        s_string("fuzzclient", fuzzable=True, max_len=20000)
    elif proto_name == "TFTP":
        s_bytes(b"\x00\x01", fuzzable=True)
        s_string("fuzzfile", fuzzable=True, max_len=20000)
    elif proto_name == "DHCP":
        s_bytes(b"\x01", fuzzable=True)
        s_bytes(b"A" * 20000, fuzzable=True)
    elif proto_name == "NETCONF":
        s_string("<hello>", fuzzable=True, max_len=20000)
        s_bytes(b"A" * 20000, fuzzable=True)
    else:
        s_string("FUZZ_DATA", fuzzable=True, max_len=20000)
        s_int(9999, fuzzable=True)
        s_bytes(b"A" * 20000, fuzzable=True)
   
    session.connect(s_get(f"{proto_name}_request"))
def fuzz_port(host, port, proto_name):
    """Perform aggressive fuzzing on a single port"""
    logger.info(f"Starting fuzzing {proto_name} (Port {port})...")
   
    connection = UDPSocketConnection(host=host, port=port) if port in udp_ports else TCPSocketConnection(host=host, port=port)
    target = Target(connection=connection)
   
    session = Session(
        target=target,
        sleep_time=0.01,  # Balanced sleep time
        crash_threshold_element=3  # Balanced threshold
    )
   
    define_protocol(session, port, proto_name)
   
    try:
        for i in range(10000):  # Reduced iterations
            session.fuzz()
            if i % 1000 == 0:  # Progress update
                logger.info(f"Completed {i} iterations on {proto_name} (Port {port})")
    except Exception as e:
        logger.error(f"Port {port} fuzzing failed: {e}")
    logger.info(f"Port {port} fuzzing complete, results in boofuzz-results/")
def main():
    if len(sys.argv) != 3:
        print("Usage: python3 chef.py <target_ip> <target_port>")
        print("Example: python3 chef.py 192.168.2.1 80")
        print("\nSupported Protocols and Ports:")
        for port, proto in ports.items():
            print(f" - {proto} ({port})")
        print("\nRun 'python3 chef.py --help' for full help menu")
        sys.exit(1)
   
    if sys.argv[1] == "--help":
        print("""
CHEF (ChillHack Easy Fuzzing) - A Boofuzz-based tool for aggressive fuzzing of network protocols.
Usage: python3 chef.py <target_ip> <target_port>
Arguments:
  target_ip The IP address of the target server (e.g., 192.168.2.1)
  target_port The port number to fuzz (e.g., 80)
Supported Protocols and Ports:
  - HTTP (80)
  - HTTPS (443)
  - HTTP-ALT (8080)
  - HTTPS-ALT (8443)
  - FTP (21)
  - SMTP (25)
  - POP3 (110)
  - IMAP (143)
  - Telnet (23)
  - DNS (53, UDP)
  - SNMP (161, UDP)
  - Modbus (502)
  - RTSP (554)
  - SIP (5060, UDP)
  - SMB (445)
  - RDP (3389)
  - MQTT (1883)
  - TFTP (69, UDP)
  - DHCP (67/68, UDP)
  - NETCONF (830)
Features:
  - Aggressive fuzzing with buffers (20,000 bytes) to trigger stack buffer overflows
  - 10000 iterations per port for high coverage, targeting zero-day vulnerabilities and crashes
  - Supports TCP and UDP protocols
  - Logs results to boofuzz-results/ directory (SQLite database)
  - Generic template for non-standard ports
Example:
  python3 chef.py 192.168.2.1 80
Output:
  - Fuzzing progress logged to console
  - Results stored in boofuzz-results/<session>.db
  - Use 'boo replay -r boofuzz-results/<session>.db' to replay crash cases
Notes:
  - Run only in authorized environments (e.g., local VM) to avoid legal issues
  - Requires Boofuzz: 'pip install boofuzz'
  - Analyze crashes with SQLite browser, Wireshark, or GDB
        """)
        sys.exit(0)
   
    host = sys.argv[1]
    try:
        port = int(sys.argv[2])
    except ValueError:
        print("Error: Port must be a number")
        sys.exit(1)
   
    proto_name = ports.get(port, "UNKNOWN")
    if proto_name == "UNKNOWN" and port not in ports:
        print(f"Warning: Port {port} is not a common protocol port, using generic fuzzing template")
   
    logger.info(f"ChillHack Easy Fuzzing (CHEF) starting, target: {host}:{port}")
    
    try:
        while True:
            fuzz_port(host, port, proto_name)
            logger.info("Restarting fuzzing cycle...")
    except KeyboardInterrupt:
        logger.info("Fuzzing interrupted by user (Ctrl+C). Stopping...")
        logger.info("Fuzzing complete, check boofuzz-results/ for SQLite database with crash or vulnerability details!")
        sys.exit(0)

if __name__ == "__main__":
    main()