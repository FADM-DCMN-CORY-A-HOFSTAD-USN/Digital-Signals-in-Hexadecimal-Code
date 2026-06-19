from ..hex_rt_infrastructure import RTGuardRing

class HexBinarySouthbridge:
    """
    The Master Translation Bridge (PCH-HX).
    Converts legacy high-voltage binary signals into pure 1V hexadecimal logic,
    and vice versa, allowing standard keyboards and mice to function.
    """
    def __init__(self):
        self.rt_guard_ring = RTGuardRing()
        # Binary to Hexadecimal Logic Mapping (4 bits -> 1 Hex Voltage State)
        self.bin_to_hex_map = {
            "0000": 0.0,    "0001": 0.0625, "0010": 0.125,  "0011": 0.1875,
            "0100": 0.25,   "0101": 0.3125, "0110": 0.375,  "0111": 0.4375,
            "1000": 0.5,    "1001": 0.5625, "1010": 0.625,  "1011": 0.6875,
            "1100": 0.75,   "1101": 0.8125, "1110": 0.875,  "1111": 1.0
        }
        # Reverse mapping for outputting to legacy devices
        self.hex_to_bin_map = {v: k for k, v in self.bin_to_hex_map.items()}

    def translate_binary_to_native_hex(self, legacy_binary_stream):
        """Ingests 3.3V/5V binary data (like a keystroke) and converts it to RT logic."""
        print(f"[SOUTHBRIDGE] Translating {len(legacy_binary_stream)} binary bits into hex voltages...")
        hex_voltage_stream = []
        
        # Process in 4-bit chunks (nibbles)
        for i in range(0, len(legacy_binary_stream), 4):
            nibble = "".join(map(str, legacy_binary_stream[i:i+4]))
            # Pad with zeros if the stream isn't perfectly divisible by 4
            if len(nibble) < 4:
                nibble = nibble.ljust(4, '0')
                
            translated_voltage = self.bin_to_hex_map.get(nibble, 0.0)
            hex_voltage_stream.append(translated_voltage)

        # Pass through the RT Guard Ring to scrub any translation noise
        return self.rt_guard_ring.isolate_logic_stream(hex_voltage_stream)

    def translate_native_hex_to_binary(self, hex_voltage_stream):
        """Converts native hex voltages back to binary for standard external devices."""
        print(f"[SOUTHBRIDGE] Down-converting RT logic back to legacy binary...")
        binary_output = []
        for voltage in hex_voltage_stream:
            # Snap to strict RT grid before translation
            snapped_v = round(voltage / 0.0625) * 0.0625
            binary_string = self.hex_to_bin_map.get(snapped_v, "0000")
            binary_output.extend([int(b) for b in binary_string])
            
        return binary_output
