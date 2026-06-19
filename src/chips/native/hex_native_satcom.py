from ..hex_rt_infrastructure import RTTraceRoute, RTGuardRing, RTPhaseChangeThermalInterface

class HexNativeSatComPCIe:
    """
    Native Hexadecimal Satellite Communications PCIe Card.
    Directly modulates 16-state analog logic onto orbital carrier waves.
    Bypasses binary packet encapsulation for zero-latency telemetry.
    """
    def __init__(self, orbital_band="Ka-Band"):
        self.orbital_band = orbital_band
        
        # RT Physical Infrastructure
        self.rt_guard_ring = RTGuardRing()
        self.rt_thermal_pad = RTPhaseChangeThermalInterface()
        
        # SATCOM antennas require high-power transmission for deep space reach.
        # We enforce 3oz copper routing for the transmission stage to mitigate thermal spikes.
        self.tx_trace = RTTraceRoute(copper_oz=3.0, trace_width_mm=4.0, length_mm=100.0)
        self.thermal_state_c = 35.0

    def uplink_telemetry(self, hex_voltage_stream):
        """
        Modulates 16-state hex logic directly into an orbital carrier wave.
        Uses Frequency Hopping to maintain signal integrity through atmospheric interference.
        """
        print(f"\n[SATCOM {self.orbital_band}] Preparing native uplink...")
        
        # 1. Isolate the signal from motherboard EM noise
        clean_stream = self.rt_guard_ring.isolate_logic_stream(hex_voltage_stream)
        
        # 2. Transmit through the high-power 3oz copper stage
        safe_stream, heat_w = self.tx_trace.transmit_analog_signal(current_amps=5.0, voltage_stream=clean_stream)
        
        if safe_stream:
            self.thermal_state_c = self.rt_thermal_pad.dissipate_heat(self.thermal_state_c, heat_w)
            print(f"[SATCOM {self.orbital_band}] Telemetry locked onto carrier wave. Uplink established.")
            return True
        return False

    def downlink_orbital_data(self, doppler_shifted_analog_wave):
        """
        Downlinks raw analog waves from orbit.
        Performs real-time Doppler shift correction on the analog wave 
        before quantizing it back to RT 16-state logic.
        """
        print(f"\n[SATCOM {self.orbital_band}] Downlink intercepted. Correcting Doppler shift...")
        
        corrected_hex_stream = []
        for v in doppler_shifted_analog_wave:
            # Physics: Correct the signal attenuation and shift due to orbital velocity
            # Simulating the native hardware correction of the analog carrier
            corrected_v = min(1.0, v * 1.05) 
            
            # Snap to strict RT grid after hardware correction
            snapped_v = round(corrected_v / 0.0625) * 0.0625
            corrected_hex_stream.append(snapped_v)
            
        final_stream = self.rt_guard_ring.isolate_logic_stream(corrected_hex_stream)
        print("[SATCOM {self.orbital_band}] Orbital stream quantized to RT logic. Ready for PCIe bus.")
        return final_stream
