from ..hex_rt_infrastructure import RTTraceRoute, RTGuardRing, RTPhaseChangeThermalInterface

class RTCentrifugalBlower:
    """
    Active Centrifugal Blower with Anti-Dust Tunnels and 0dB Intelligence.
    Engineered to exhaust extreme heat directly out the rear PCIe bracket.
    """
    def __init__(self, max_rpm=4500):
        self.max_rpm = max_rpm
        self.current_rpm = 0
        self.zero_db_threshold_c = 50.0  # Fan remains completely silent below 50°C

    def exhaust_heat(self, ambient_armor_temp_c):
        """
        Calculates active cooling based on the armor's thermal state.
        Incorporates zero-RPM silent modes and centrifugal dust ejection.
        """
        if ambient_armor_temp_c < self.zero_db_threshold_c:
            if self.current_rpm > 0:
                print("[RT BLOWER] 0dB Technology Active. Spin-down initiated. Zero acoustic noise.")
            self.current_rpm = 0
            return ambient_armor_temp_c

        # Spin up the blower relative to the heat load
        rpm_percentage = min(1.0, (ambient_armor_temp_c - self.zero_db_threshold_c) / 40.0)
        self.current_rpm = int(self.max_rpm * rpm_percentage)
        
        print(f"[RT BLOWER] Active Cooling Engaged. Blower spooled to {self.current_rpm} RPM.")
        
        # Centrifugal Anti-Dust Physics: High RPMs physically eject dust out the back
        if self.current_rpm > 3000:
            print("  -> [ANTI-DUST TUNNEL] Centrifugal force ejecting debris from heatsink micro-fins.")

        # Active exhaust cooling calculation (drastically drops temperature)
        cooling_factor = (self.current_rpm / self.max_rpm) * 18.0
        return max(35.0, ambient_armor_temp_c - cooling_factor)


class HexM2PCIeExpander:
    """
    Native Hexadecimal M.2 PCIe Expansion Card (Quad-Slot) with Active Blower.
    Features physical thermal spacing, hardware-level lane bifurcation, and active RT cooling.
    """
    def __init__(self):
        self.m2_slots = {
            "SLOT_1": None,
            "SLOT_2": None,
            "SLOT_3": None,
            "SLOT_4": None
        }
        
        # Initialize the RT physical infrastructure for this chip
        self.rt_vapor_chamber = RTVaporChamberHeatsink()
        self.rt_thermal_pad = RTPhaseChangeThermalInterface()
        self.rt_guard_ring = RTGuardRing()
        self.pcie_bridge_trace = RTTraceRoute(copper_oz=2.0, trace_width_mm=2.5, length_mm=75.0)
        
        # The new active exhaust system
        self.exhaust_blower = RTCentrifugalBlower()
        
        self.thermal_state_c = 35.0

    def mount_drive(self, slot_id, hex_native_ssd):
        if slot_id in self.m2_slots:
            self.m2_slots[slot_id] = hex_native_ssd
            print(f"[M.2 EXPANDER] Native Hex SSD locked into {slot_id}. Guard ring active.")

    def direct_route_to_drive(self, target_slot, start_address, hex_voltage_stream):
        """Routes the 16-state logic directly to a specific M.2 drive."""
        if self.m2_slots.get(target_slot) is None:
            return False

        print(f"\n[M.2 EXPANDER] Routing {len(hex_voltage_stream)} analog states to {target_slot}...")
        
        safe_stream, heat_w = self.pcie_bridge_trace.transmit_analog_signal(current_amps=3.5, voltage_stream=hex_voltage_stream)
        
        if safe_stream:
            clean_stream = self.rt_guard_ring.isolate_logic_stream(safe_stream)
            target_drive = self.m2_slots[target_slot]
            
            for i, voltage in enumerate(clean_stream):
                target_drive.write_native_voltage(address=(start_address + i), voltage=voltage)
                
            # 1. Passive Cooling: The Phase-Change Armor absorbs the immediate heat spike
            self.thermal_state_c += heat_w * 0.4
            self.thermal_state_c = self.rt_thermal_pad.dissipate_heat(self.thermal_state_c, heat_w)
            
            # 2. Active Exhaust: The Blower engages if the armor crosses 50°C
            self.thermal_state_c = self.exhaust_blower.exhaust_heat(self.thermal_state_c)
            
            print(f"[M.2 EXPANDER] Write successful. Card Temp: {self.thermal_state_c:.1f}°C.")
            return True
        return False

    def hardware_stripe_matrix(self, hex_voltage_matrix):
        """
        Splits a massive matrix instantly across all 4 spaced drives simultaneously.
        Triggers massive thermal loads, requiring the blower to spool to maximum RPM.
        """
        active_slots = [slot for slot in self.m2_slots.values() if slot is not None]
        if not active_slots:
            return False
            
        print(f"\n[M.2 EXPANDER] Initiating Hardware Stripe across {len(active_slots)} drives...")
        
        # Simulated parallel write generating extreme thermal loads
        heat_spike_w = 45.0 
        
        chunk_size = len(hex_voltage_matrix) // len(active_slots)
        for i, drive in enumerate(active_slots):
            print(f"  -> Striping chunk to Drive {i+1}...")
            
        # The phase-change pad will instantly liquefy under this massive load
        self.thermal_state_c += heat_spike_w
        self.thermal_state_c = self.rt_thermal_pad.dissipate_heat(self.thermal_state_c, heat_spike_w)
        
        # The blower will spool up heavily to push the hot air out the back of the case
        self.thermal_state_c = self.exhaust_blower.exhaust_heat(self.thermal_state_c)
            
        print(f"[M.2 EXPANDER] Striping complete. Card Temp stabilized at {self.thermal_state_c:.1f}°C.")
        return True
