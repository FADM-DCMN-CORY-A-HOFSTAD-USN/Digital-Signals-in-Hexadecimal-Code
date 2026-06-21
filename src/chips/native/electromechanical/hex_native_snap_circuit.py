"""
Hexadecimal Snap-Circuit (Double Latch Gate Buffer)
Maintains a quantum-entangled link via 24k gold lattice chemical bonds.
Form Factor: Modular Breakaway PCB Enclosure
"""

class HexNativeSnapCircuit:
    def __init__(self, node_id: str):
        self.device_id = f"SNAP_CIRCUIT_NODE_{node_id}"
        self.latch_top = "0x00"  
        self.latch_bottom = "0x00" 
        self.is_snapped = False
        self.entangled_partner = None

    def physical_snap(self, partner_node):
        """Simulates the physical fracture of the gold lattice, locking the quantum state."""
        self.is_snapped = True
        self.entangled_partner = partner_node
        print(f"[{self.device_id}] LATTICE FRACTURED. Quantum bond preserved with {partner_node.device_id}.")
        return "ENTANGLEMENT_LOCKED"

    def _cross_couple_invert(self, hex_val: str) -> str:
        """
        The core latch mechanism. Inverts the hex signal, then re-inverts it to stabilize.
        In a true hex optical system, this creates the stable memory buffer.
        """
        int_val = int(hex_val, 16)
        inverted = ~int_val & 0xFFFFFFFFFFFFFFFF 
        re_inverted = ~inverted & 0xFFFFFFFFFFFFFFFF
        return hex(re_inverted)

    def transmit_buffer(self, hex_payload: str):
        """Pushes the payload buffer across the quantum gap to the remote node."""
        if not self.is_snapped or not self.entangled_partner:
            return "ERROR: LATTICE NOT SNAPPED"

        # Latch the data locally into the top and bottom inverters
        self.latch_top = self._cross_couple_invert(hex_payload)
        self.latch_bottom = self.latch_top 

        print(f"[{self.device_id}] Buffer Latched: {self.latch_top}")
        print(f"[{self.device_id}] Transmitting across quantum gap...")

        # Instantaneous remote update
        self.entangled_partner.receive_buffer(self.latch_top)
        return "TRANSMISSION_COMPLETE"

    def receive_buffer(self, hex_payload: str):
        """Receives the instantaneous state change from the entangled partner."""
        self.latch_top = hex_payload
        self.latch_bottom = hex_payload
        print(f"[{self.device_id}] Quantum Shift Detected. New Buffer State: {self.latch_top}")

    def trigger_morse_pulse(self):
        """Manual finger-touch pulse for emergency signaling."""
        print(f"[{self.device_id}] Manual pulse triggered.")
        self.transmit_buffer("0xFFFFFFFFFFFFFFFF") # Send peak intensity flash
