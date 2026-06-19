import json

class HexRAM:
    """
    High-Density Hexadecimal Random Access Memory (RAM).
    Stores data as 16-state discrete voltages (0.0V - 1.0V) rather than binary bits.
    """
    def __init__(self, capacity_bytes, logic_file_path='../src/logic_levels.json'):
        self.capacity = capacity_bytes
        # Each memory address holds a single hex character (0-F) represented by voltage
        self.memory_cells = ['0'] * self.capacity 
        
        # Load the 1V logic tolerances
        with open(logic_file_path, 'r') as file:
            self.logic_map = json.load(file)['1V_logic']
            
    def write(self, address, hex_value):
        """Writes a hex value to a specific memory address."""
        hex_value = str(hex_value).upper()
        if 0 <= address < self.capacity and hex_value in self.logic_map:
            self.memory_cells[address] = hex_value
            voltage = self.logic_map[hex_value]
            print(f"[RAM WRITE] Addr {address}: Stored {hex_value} at {voltage}V")
        else:
            raise ValueError("Invalid memory address or Hex value out of bounds.")

    def read_voltage(self, address):
        """Reads the raw voltage stored at the memory address."""
        if 0 <= address < self.capacity:
            hex_value = self.memory_cells[address]
            return self.logic_map[hex_value]
        return None

# Example usage for testing
if __name__ == "__main__":
    ram_module = HexRAM(capacity_bytes=1024) # 1KB Hex RAM
    ram_module.write(address=0x0A, hex_value='C') # Stores 0.8125V
