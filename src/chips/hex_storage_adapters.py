import json

class HexLegacyAdapter:
    """Base class for translating legacy binary drive protocols into 16-state Hex-PCIe logic."""
    def __init__(self, protocol="IDE"):
        self.protocol = protocol
        # Safe voltage step-down ratios for forensic extraction
        self.voltage_step_down = 5.0 if protocol in ["IDE", "SCSI"] else 3.3

    def forensic_read_sector(self, sector_data_binary):
        """Translates high-voltage binary states into safe 0.0625V increment logic."""
        print(f"[{self.protocol} ADAPTER] Reading physical sector. Stepping down {self.voltage_step_down}V logic...")
        # Simulating the translation of 4 binary bits into a single Hex analog voltage
        translated_hex_stream = []
        for i in range(0, len(sector_data_binary), 4):
            chunk = sector_data_binary[i:i+4]
            hex_val = int("".join(map(str, chunk)), 2)
            translated_hex_stream.append(hex_val * 0.0625)
        return translated_hex_stream

class HexM2Adapter:
    """High-speed NVMe to Hex-PCIe bridge for modern SSD arrays."""
    def __init__(self):
        self.protocol = "M.2_NVMe"
        self.lane_speed_gbps = 64.0

    def direct_memory_access_transfer(self, target_ram_address, hex_data_stream):
        print(f"[M.2 ADAPTER] Bypassing CPU. DMA streaming {len(hex_data_stream)} hex states to RAM address {target_ram_address}.")
        return True
