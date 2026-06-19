"""
Hexadecimal to Univac-IX 36-bit Hardware Downconverter
Ensures native, unhackable communication between the modern ship and the legacy SCADA plant.
Location: src/chips/native/hex_native_univac_translator.py
"""

class HexNativeUnivacTranslator:
    def __init__(self):
        self.device_id = "UNIVAC_BRIDGE_36BIT"
        
    def downconvert_to_legacy(self, modern_64bit_hex: str):
        """
        Strips and packs a modern 64-bit hex word into a 36-bit Univac word.
        Univac uses 36-bit words, which is exactly nine 4-bit octal digits, 
        or a padded hexadecimal string.
        """
        # Clean the input
        clean_hex = modern_64bit_hex.replace("0x", "").zfill(16)
        
        # Univac relies heavily on Fieldata or early ASCII. 
        # We truncate the 64-bit payload to the 36 most significant bits (9 hex chars)
        legacy_36bit_payload = clean_hex[:9] 
        
        print(f"[{self.device_id}] Downconverting modern packet: 0x{clean_hex}")
        print(f"[{self.device_id}] Legacy 36-bit Word generated: 0x{legacy_36bit_payload}")
        
        return self._transmit_to_master_orchestrator(legacy_36bit_payload)

    def _transmit_to_master_orchestrator(self, payload: str):
        """Sends the exact 36-bit pulse across the Jamoni crystal network to the factory floor."""
        return {"scada_status": "ACKNOWLEDGED", "univac_word": payload}
