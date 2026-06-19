import json

class HexSSD:
    """Solid State Drive storing Hexadecimal voltage states in NAND cells."""
    def __init__(self, capacity_blocks):
        self.capacity = capacity_blocks
        self.storage_array = ['0'] * self.capacity

    def write_block(self, address, hex_value):
        self.storage_array[address] = str(hex_value).upper()

class HexRAIDController:
    """
    Hardware RAID Controller with NVRAM cache and Battery Backup Unit (BBU).
    Designed to protect analog hexadecimal states during power failure.
    """
    def __init__(self, raid_level=5):
        self.raid_level = raid_level
        self.drives = []
        self.nvram_cache = []
        self.battery_level = 100.0  # Percentage
        self.cache_flushed = True

    def attach_drive(self, hex_ssd, interface="SAS"):
        """Supports Hex-adapted M.2, SAS, SATA, SCSI, and IDE protocols."""
        self.drives.append({"drive": hex_ssd, "interface": interface})
        print(f"[RAID] Attached drive via {interface} interface.")

    def write_with_cache(self, data_stream):
        """Writes incoming Hex states to cache, pending destage to physical drives."""
        self.nvram_cache.extend(data_stream)
        self.cache_flushed = False
        print(f"[RAID] Cached {len(data_stream)} Hex states. Battery at {self.battery_level}%.")

    def forensic_preserve_state(self):
        """
        Freezes cache and suspends parity calculations for clean data extraction,
        crucial for post-failure array recovery and chip-level forensics.
        """
        if not self.cache_flushed and self.battery_level > 5.0:
            print("[RAID] FORENSIC LOCK: NVRAM cache preserved by battery backup. Ready for extraction.")
            return self.nvram_cache
        return []
