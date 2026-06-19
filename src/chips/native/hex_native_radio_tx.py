from ..hex_rt_infrastructure import RTTraceRoute, RTPhaseChangeThermalInterface

class HexNativeRadioTransmitter:
    """
    Native Hexadecimal Radio Frequency Transmitter (TX-HX).
    Modulates native 16-state RT logic directly onto a high-power RF carrier wave.
    """
    def __init__(self, carrier_frequency_mhz=433.0, tx_power_watts=50.0):
        self.frequency = carrier_frequency_mhz
        self.transmission_power = tx_power_watts
        
        # Pushing 50+ Watts of RF power requires massive trace infrastructure
        self.amplifier_trace = RTTraceRoute(copper_oz=2.0, trace_width_mm=3.5, length_mm=60.0)
        self.rt_thermal_pad = RTPhaseChangeThermalInterface()
        self.thermal_state_c = 40.0

    def broadcast_hex_telemetry(self, hex_voltage_stream):
        """
        Takes analog logic from the PCIe bus and amplifies it into a physical radio wave.
        Uses Amplitude Modulation (AM) where Hex F (1.0V) equals maximum broadcast power.
        """
        print(f"\n[RADIO TX {self.frequency}MHz] Preparing to broadcast {len(hex_voltage_stream)} telemetry states...")
        
        # 1. Push current through the RT Trace to the RF Amplifier
        # 50W broadcast at typical voltages can draw significant amperage
        draw_amps = self.transmission_power / 12.0 
        safe_stream, heat_w = self.amplifier_trace.transmit_analog_signal(draw_amps, hex_voltage_stream)
        
        if not safe_stream:
            print("[RADIO TX] BROADCAST HALTED. RF Amplifier trace bottleneck detected.")
            return False

        # 2. Modulate and Broadcast
        broadcast_wave = []
        for voltage in safe_stream:
            # Scale the 0.0V-1.0V logic into actual transmitted RF wattage
            rf_pulse_wattage = voltage * self.transmission_power
            broadcast_wave.append(rf_pulse_wattage)
            
        # 3. Handle Extreme Heat Dump from the Amplifier
        self.thermal_state_c += heat_w * 0.5
        self.thermal_state_c = self.rt_thermal_pad.dissipate_heat(self.thermal_state_c, heat_w)
        
        print(f"[RADIO TX] Broadcast complete. Signal propelled into atmosphere. Thermal State: {self.thermal_state_c:.1f}°C")
        return broadcast_wave
