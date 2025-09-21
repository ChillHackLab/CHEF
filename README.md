# CHEF: ChillHack Easy Fuzzing

**CHEF (ChillHack Easy Fuzzing)** is a powerful, versatile network protocol fuzzing tool developed by **ChillHack Hong Kong Web Development**. Designed as a Swiss Army knife for security researchers and penetration testers, CHEF enables aggressive fuzzing of various network protocols to uncover vulnerabilities, such as stack buffer overflows and zero-day exploits, in a controlled and authorized environment.

- **Developer**: ChillHack Hong Kong Web Development
- **Email**: [info@chillhack.net](mailto:info@chillhack.net)
- **Website**: [https://chillhack.net](https://chillhack.net)
- **License**: MIT License

## Features

- **Multi-Protocol Support**: Fuzz a wide range of protocols including HTTP, HTTPS, FTP, SMTP, POP3, IMAP, Telnet, DNS, SNMP, Modbus, RTSP, SIP, SMB, RDP, MQTT, TFTP, DHCP, and NETCONF, with a generic template for non-standard ports.
- **Aggressive Fuzzing**: Configurable with 10,000 iterations per cycle, 20,000-byte payloads, and a 0.01-second sleep interval to maximize vulnerability detection.
- **TCP and UDP Compatibility**: Seamlessly handles both TCP and UDP protocols, automatically selecting the appropriate connection type based on the target port.
- **Continuous Operation**: Runs indefinitely until interrupted with `Ctrl+C`, ensuring exhaustive testing with automatic cycle restarts.
- **Crash Detection**: Configurable crash threshold (default: 3 consecutive failures) to identify potential vulnerabilities with high accuracy.
- **Detailed Logging**: Saves fuzzing results to an SQLite database in the `boofuzz-results/` directory for post-analysis using tools like SQLite browser, Wireshark, or GDB.
- **User-Friendly Interface**: Simple command-line usage with a comprehensive help menu and progress indicators for real-time feedback.

## Supported Protocols and Ports

| Protocol       | Port(s)       | Transport |
|----------------|---------------|-----------|
| HTTP           | 80, 8080      | TCP       |
| HTTPS          | 443, 8443     | TCP       |
| FTP            | 21            | TCP       |
| SMTP           | 25            | TCP       |
| POP3           | 110           | TCP       |
| IMAP           | 143           | TCP       |
| Telnet         | 23            | TCP       |
| DNS            | 53            | UDP       |
| SNMP           | 161           | UDP       |
| Modbus         | 502           | TCP       |
| RTSP           | 554           | TCP       |
| SIP            | 5060          | UDP       |
| SMB            | 445           | TCP       |
| RDP            | 3389          | TCP       |
| MQTT           | 1883          | TCP       |
| TFTP           | 69            | UDP       |
| DHCP           | 67, 68        | UDP       |
| NETCONF        | 830           | TCP       |

For unsupported ports, CHEF applies a generic fuzzing template to maximize versatility.

## Installation

### Prerequisites
- **Python 3.6+**: Ensure Python 3 is installed on your system.
- **Boofuzz**: The core fuzzing library used by CHEF.

### Steps
1. **Install Python**:
   - Download and install Python 3 from [python.org](https://www.python.org/downloads/) if not already installed.
   - Verify installation: `python3 --version`

2. **Install Boofuzz**:
   ```bash
   pip install boofuzz
   ```

3. **Download CHEF**:
   - Clone or download the CHEF repository from [GitHub](#) (replace with actual repository URL if available) or use the provided `chef.py` script.
   - Save the script to a local directory (e.g., `chef.py`).

4. **Verify Setup**:
   - Ensure you have write permissions in the working directory for the `boofuzz-results/` folder, where results are stored.

## Usage

### Basic Command
```bash
python3 chef.py <target_ip> <target_port>
```

- `<target_ip>`: The IP address of the target server (e.g., `192.168.2.1`).
- `<target_port>`: The port number to fuzz (e.g., `80` for HTTP).

### Example
To fuzz an HTTP server running on `192.168.2.1:80`:
```bash
python3 chef.py 192.168.2.1 80
```

### Help Menu
Access the detailed help menu for supported protocols and usage instructions:
```bash
python3 chef.py --help
```

### Stopping the Script
CHEF runs continuously, restarting after each fuzzing cycle. To stop, press `Ctrl+C`. Results are saved in the `boofuzz-results/` directory.

### Output
- **Console**: Displays real-time progress, including iteration counts and errors.
- **Results**: Stored in an SQLite database (`boofuzz-results/<session>.db`) for detailed analysis.
- **Replay Crashes**: Use the `boo` command to replay crash cases:
  ```bash
  boo replay -r boofuzz-results/<session>.db
  ```

## Configuration

The default configuration is optimized for balance between aggressiveness and usability:
- **Iterations**: 10,000 per cycle.
- **Sleep Time**: 0.01 seconds between requests.
- **Payload Size**: 20,000 bytes for large buffer attacks.
- **Crash Threshold**: 3 consecutive failures to mark a crash.

To modify these settings, edit the `fuzz_port` and `define_protocol` functions in `chef.py`. For example:
- Reduce iterations: Change `range(10000)` to `range(5000)` in `fuzz_port`.
- Increase payload size: Update `s_bytes(b"A" * 20000)` to `s_bytes(b"A" * 50000)` in `define_protocol`.

## Notes

- **Legal Warning**: CHEF is a powerful fuzzing tool that can disrupt or crash target systems. Use **only in authorized environments** (e.g., local VMs or systems you own) to avoid legal issues.
- **Performance**: The aggressive settings may consume significant CPU, memory, and network resources. Monitor your system and target to avoid unintended consequences.
- **Analysis**: Use tools like SQLite browser, Wireshark, or GDB to analyze crash data in `boofuzz-results/`.
- **Troubleshooting**:
  - If the terminal appears unresponsive, reduce logging verbosity (e.g., set `logging.basicConfig(level=logging.ERROR)`).
  - Redirect logs to a file: `logging.basicConfig(filename='fuzzing.log', level=logging.INFO)`.
  - Ensure the target is reachable (`ping <host>` or `nc -zv <host> <port>`).

## Contributing

We welcome contributions to enhance CHEF’s functionality! To contribute:
1. Fork the repository (replace with actual repository URL if available).
2. Create a feature branch (`git checkout -b feature/new-feature`).
3. Commit your changes (`git commit -m "Add new feature"`).
4. Push to the branch (`git push origin feature/new-feature`).
5. Submit a pull request.

For bug reports or feature requests, contact us at [info@chillhack.net](mailto:info@chillhack.net).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For support or inquiries, reach out to:
- **Email**: [info@chillhack.net](mailto:info@chillhack.net)
- **Website**: [https://chillhack.net](https://chillhack.net)

Developed with ❤️ by **ChillHack Hong Kong Web Development**. Happy fuzzing!
