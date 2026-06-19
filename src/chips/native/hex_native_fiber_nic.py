from ..hex_rt_infrastructure import RTTraceRoute, RTGuardRing, RTPhaseChangeThermalInterface

class HexNativeFiberNIC:
    """
    Native Hexadecimal Fiber Optic Network Interface Card (NIC-HX).
    Transmits and receives pure 16-state logic over silica fiber by modulating 
    analog laser intensity, completely bypassing binary packet encapsulation.
    """
    def __init__(self, mac_address="RT:HX:00:01:A4"):
        self.mac_address = mac_address
        self.link_status = "100_GHx_ACTIVE" # Gigahashes/Gigahertz Hexadecimal Link
        
        # RT Infrastructure
        self.rt_guard_ring = RTGuardRing()
        self.rt_thermal_pad = RTPhaseChangeThermalInterface()
        
        # High-speed data routing to the PCIe bus requires thick traces to prevent heat
        self.pcie_bus_trace = RTTraceRoute(copper_oz=2.0, trace_width_mm=1.5, length_mm=35.0)
        
        self.thermal_state_c = 32.0
        
        # Optoelectronic mapping (1.0V max logic = 10.0mW max optical output)
        self.voltage_to_mw_multiplier = 10.0 

    def transmit_native_packet(self, hex_voltage_stream):
        """
        Converts the 0.0V - 1.0V analog electrical signals from the PCIe bus 
        directly into corresponding optical intensities for the transmitting laser.
        """
        print(f"\n[NATIVE FIBER NIC] Preparing outbound payload of {len(hex_voltage_stream)} hex states...")
        
        # Push the data through the RT trace to ensure the PCIe bus isn't bottlenecking
        safe_stream, heat_w = self.pcie_bus_trace.transmit_analog_signal(current_amps=1.2, voltage_stream=hex_voltage_stream)
        
        if not safe_stream:
            print("[NATIVE FIBER NIC] TX FAULT. Trace bottleneck prevented transmission.")
            return None
            
        optical_transmission_stream = []
        for voltage in safe_stream:
            # Scale the voltage into raw optical laser power (milliwatts)
            # Hex F (1.0V) fires the laser at a blinding 10.0mW
            # Hex 7 (0.5V) fires the laser at 5.0mW
            optical_mw = voltage * self.voltage_to_mw_multiplier
            optical_transmission_stream.append(optical_mw)
            
        print(f"[NATIVE FIBER NIC] Firing transmission laser. Payload traversing fiber core.")
        return optical_transmission_stream

    def receive_optical_packet(self, optical_intensity_stream):
        """
        Ingests incoming light pulses from the network, converts them back to voltage, 
        and acts as an invincible physical hardware firewall against network floods.
        """
        print(f"\n[NATIVE FIBER NIC] Incoming optical packet detected. Converting to electrical RT logic...")
        
        raw_electrical_stream = []
        for optical_mw in optical_intensity_stream:
            # Convert incoming optical power back down to the 1V logic scale
            voltage_equivalent = optical_mw / self.voltage_to_mw_multiplier
            raw_electrical_stream.append(voltage_equivalent)

        # =====================================================================
        # THE HARDWARE FIREWALL (RT Guard Ring Execution)
        # =====================================================================
        # If an attacker attempts to DDoS the server by sending malformed or 
        # blindingly bright optical pulses (e.g., an 11.0mW surge), the voltage 
        # equivalent will exceed the strict 1.0V (Hex F) architectural limit.
        # The RT Guard Ring acts as a physical moat, instantly intercepting and 
        # grounding any anomaly before it can cross onto the motherboard's PCIe bus.
        
        secure_stream = []
        dropped_packets = 0
        
        for v in raw_electrical_stream:
            if v > 1.0 or v < 0.0:
                # Malicious or anomalous surge detected. Ground it immediately.
                dropped_packets += 1
                continue
                
            # Snap valid signals perfectly to the 0.0625V intervals
            snapped_v = round(v / 0.0625) * 0.0625
            secure_stream.append(snapped_v)

        if dropped_packets > 0:
            print(f"[SECURITY LOCK] Hardware firewall dropped {dropped_packets} malicious analog surges.")
            
        # Scrub the remaining safe data through the Guard Ring for crosstalk
        final_clean_stream = self.rt_guard_ring.isolate_logic_stream(secure_stream)
        
        print(f"[NATIVE FIBER NIC] Passed {len(final_clean_stream)} secure hex states to motherboard PCIe bus.")
        return final_clean_stream
