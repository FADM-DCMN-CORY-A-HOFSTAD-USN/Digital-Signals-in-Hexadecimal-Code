class HexPCIeBus:
    """
    High-bandwidth Hexadecimal Peripheral Component Interconnect Express (Hex-PCIe).
    Routes 16-state analog logic voltages between system components.
    """
    def __init__(self, lanes=16):
        self.lanes = lanes
        self.connected_devices = {}
        
    def plug_device(self, device_id, device_object):
        """Connects a Hex card to the PCIe bus."""
        self.connected_devices[device_id] = device_object
        print(f"[Hex-PCIe] Device '{device_id}' registered on the bus.")

    def transmit(self, source_id, target_id, hex_voltage_stream):
        """Routes a stream of logic voltages from one device to another."""
        if target_id in self.connected_devices:
            print(f"[Hex-PCIe] Routing {len(hex_voltage_stream)} hex states from {source_id} to {target_id}...")
            # In a physical board, this is where signal integrity and capacitance matter most
            return self.connected_devices[target_id].receive_data(hex_voltage_stream)
        else:
            print(f"[Hex-PCIe] ERROR: Target '{target_id}' not found on bus.")
            return None
