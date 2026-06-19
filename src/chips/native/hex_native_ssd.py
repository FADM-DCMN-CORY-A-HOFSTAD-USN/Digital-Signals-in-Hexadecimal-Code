class HexNativeSSD:
    """
    Pure 16-State Solid State Drive.
    NAND cells natively hold a discrete voltage charge (0.0V - 1.0V).
    """
    def __init__(self, capacity_hex_blocks=4096):
        self.capacity = capacity_hex_blocks
        # Stores raw floating point voltages, no binary bits
        self.nand_array = [0.0] * self.capacity 

    def write_native_voltage(self, address, voltage):
        """Injects the exact 0.0625V-increment charge into the cell."""
        if 0 <= address < self.capacity:
            self.nand_array[address] = voltage
            print(f"[NATIVE SSD] Stored {voltage}V charge at block {address}.")

    def chip_off_forensic_read(self, address):
        """
        Bypasses the controller to read the raw analog charge directly from the 
        silicon substrate for extreme hardware forensics and array rebuilding.
        """
        raw_charge = self.nand_array[address]
        print(f"[FORENSICS] Extracted raw substrate charge: {raw_charge}V.")
        return raw_charge
