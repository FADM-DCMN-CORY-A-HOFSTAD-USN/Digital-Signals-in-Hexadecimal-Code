from ..hex_rt_infrastructure import RTTraceRoute, RTGuardRing, RTPhaseChangeThermalInterface

class HexAnalogPMIC:
    """
    Native Hexadecimal Power Management IC (PMIC-HX).
    DDR5 exclusive: Moves power regulation from the motherboard directly onto the DIMM.
    Steps down heavy 12V trace power into the flawless 0.0625V intervals required for memory retention.
    """
    def __init__(self):
        self.input_voltage = 12.0
        self.logic_reference_voltage = 1.0 # Max Hex F
        self.rt_guard_ring = RTGuardRing()

    def regulate_dimm_power(self, raw_motherboard_current):
        """Creates an ultra-clean isolated power plane directly on the RAM stick."""
        # Scrub the incoming raw power through the Guard Ring before it touches the analog memory cells
        clean_baseline = self.rt_guard_ring.isolate_logic_stream([self.logic_reference_voltage])[0]
        return clean_baseline


class HexNativeDDR5_DIMM:
    """
    Native Hexadecimal DDR5 Vertical Memory Module (DIMM-HX).
    Features a centered physical structural key, dual-channel analog routing, 
    and onboard PMIC voltage step-down.
    """
    def __init__(self, capacity_hex_blocks=524288):
        self.capacity = capacity_hex_blocks
        
        # DDR5 Architecture: 2 parallel sub-channels per stick (replacing 2x 32-bit binary)
        self.sub_channels = 2 
        self.memory_cells_ch_a = [0.0] * (self.capacity // 2)
        self.memory_cells_ch_b = [0.0] * (self.capacity // 2)
        
        # Physical Form Factor (DDR5 Specifications)
        self.dimensions_mm = {"length": 133.35, "z_height": 31.25, "pins": 288, "pitch": 0.85}
        self.key_notch_center_mm = 66.675 # Absolute center
        self.is_seated = False
        
        # Onboard Sub-components
        self.onboard_pmic = HexAnalogPMIC()
        self.rt_thermal_pad = RTPhaseChangeThermalInterface()
        self.thermal_state_c = 42.0 # Runs hotter natively due to the onboard PMIC

    def insert_into_slot(self, motherboard_slot_notch_mm):
        """
        Mechanically inserts the 288-pin analog module into the motherboard slot.
        The centered key notch physically prevents DDR4 insertion.
        """
        if motherboard_slot_notch_mm == self.key_notch_center_mm:
            self.is_seated = True
            print(f"\n[DDR5-HX DIMM] Module seated correctly. 288 analog pins engaged.")
            print(f"  -> Structural alignment: {self.dimensions_mm['length']}mm length, Notch at {self.key_notch_center_mm}mm.")
            
            # Initialize onboard power
            reference_v = self.onboard_pmic.regulate_dimm_power(raw_motherboard_current=1.5)
            print(f"  -> Onboard PMIC initialized. Stable {reference_v}V logic plane established.")
            return True
        else:
            print("[DDR5-HX DIMM] MECHANICAL FAULT: Key notch misalignment. Halting insertion to prevent pin damage.")
            return False

    def write_dual_channel_hex(self, start_address, hex_stream_a, hex_stream_b):
        """
        Executes a simultaneous parallel write across both independent analog channels.
        Doubles the bandwidth efficiency compared to older single-channel DIMMs.
        """
        if not self.is_bolted_and_powered():
            return False
            
        print(f"[DDR5-HX DIMM] Writing parallel analog streams (Ch. A: {len(hex_stream_a)} states, Ch. B: {len(hex_stream_b)} states)...")
        
        # Channel A Route
        for i, voltage in enumerate(hex_stream_a):
            if (start_address + i) < len(self.memory_cells_ch_a):
                self.memory_cells_ch_a[start_address + i] = voltage
                
        # Channel B Route
        for i, voltage in enumerate(hex_stream_b):
            if (start_address + i) < len(self.memory_cells_ch_b):
                self.memory_cells_ch_b[start_address + i] = voltage

        # Thermal Physics: DDR5's onboard PMIC generates localized heat on the stick itself
        heat_spike_w = (len(hex_stream_a) + len(hex_stream_b)) * 0.08
        self.thermal_state_c += heat_spike_w
        self.thermal_state_c = self.rt_thermal_pad.dissipate_heat(self.thermal_state_c, heat_spike_w)
        
        return True

    def is_bolted_and_powered(self):
        if not self.is_seated:
            print("[DDR5-HX DIMM] FAULT: DIMM not fully seated in motherboard slot.")
            return False
        return True
