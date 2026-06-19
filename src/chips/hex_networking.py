class HexNetworkInterface:
    """Base class for Hexadecimal Network Cards (Fiber, WiFi, Cellular)."""
    def __init__(self, mac_address, media_type="FIBER_OPTIC"):
        self.mac_address = mac_address
        self.media_type = media_type
        self.link_active = True

    def receive_data(self, incoming_stream):
        """Hardware-level packet inspection."""
        if self.media_type == "FIBER_OPTIC":
            # Hardware-accelerated filtering to drop anomalous packet streams 
            # (e.g., stopping SYN floods before hitting the software firewall)
            clean_stream = self._hardware_firewall_filter(incoming_stream)
            print(f"[NET - {self.media_type}] Passed {len(clean_stream)} secure Hex states to bus.")
            return clean_stream
        
        print(f"[NET - {self.media_type}] Received wireless stream.")
        return incoming_stream

    def _hardware_firewall_filter(self, stream):
        # Drops any analog signal exceeding 1.0V as hardware anomaly/malicious
        return [v for v in stream if v <= 1.0]

class HexPeripheralController:
    """Manages external user interfaces like USB ports, Serial cards, and Bluetooth."""
    def __init__(self):
        self.usb_ports = 4
        self.serial_active = True
        self.bluetooth_paired = False

    def receive_data(self, usb_input_voltage):
        print(f"[USB/SERIAL IO] Ingested peripheral logic level: {usb_input_voltage}V")
