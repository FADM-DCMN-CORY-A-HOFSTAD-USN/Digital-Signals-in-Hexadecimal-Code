class HexLegacyEthernetPHY:
    """
    10GBASE-T Copper Ethernet Adapter.
    Bridges the native Hex-PCIe bus to the standard global binary internet.
    """
    def __init__(self, mac_address):
        self.mac_address = mac_address
        self.link_speed = "10_Gbps"

    def transmit_tcp_ip_packet(self, hex_payload, southbridge):
        """Uses the Southbridge to convert the packet before sending to the RJ45 port."""
        print(f"[ETHERNET PHY] Preparing native packet for standard TCP/IP transmission.")
        
        # Offload translation to the Southbridge
        binary_payload = southbridge.translate_native_hex_to_binary(hex_payload)
        
        print(f"[ETHERNET PHY] Transmitting {len(binary_payload)} binary bits over copper line.")
        return True

    def receive_tcp_ip_packet(self, binary_payload, southbridge):
        print(f"[ETHERNET PHY] Receiving legacy binary packet from copper line.")
        hex_payload = southbridge.translate_binary_to_native_hex(binary_payload)
        return hex_payload
