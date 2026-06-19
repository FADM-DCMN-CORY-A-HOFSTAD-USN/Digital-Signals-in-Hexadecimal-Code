from ..hex_rt_infrastructure import RTGuardRing

class HexNativeRadioReceiver:
    """
    Native Hexadecimal Radio Frequency Receiver (RX-HX).
    Captures weak atmospheric RF waves and quantizes them back into strict RT logic.
    """
    def __init__(self, carrier_frequency_mhz=433.0):
        self.frequency = carrier_frequency_mhz
        
        # The Guard Ring acts as a physical hardware squelch/filter to drop atmospheric noise
        self.rt_guard_ring = RTGuardRing()
        
        # Signals below this ambient threshold are dropped as background static
        self.squelch_threshold_v = 0.05 

    def intercept_rf_signal(self, atmospheric_rf_wave, transmitter_power_watts=50.0):
        """
        Ingests a continuous analog radio wave from the antenna and steps it back down 
        into the 16-state logic required by the Z-Series motherboard.
        """
        print(f"\n[RADIO RX {self.frequency}MHz] Intercepting atmospheric radio wave...")
        
        raw_electrical_stream = []
        for received_wattage in atmospheric_rf_wave:
            # 1. Demodulate: Step the received RF wattage back down to the 1V logic scale
            voltage_equivalent = received_wattage / transmitter_power_watts
            
            # 2. Squelch: Ignore random cosmic static
            if voltage_equivalent < self.squelch_threshold_v:
                continue
                
            raw_electrical_stream.append(voltage_equivalent)

        # 3. The RT Guard Ring Hardware Filter
        # Atmospheric interference will cause the voltage to fluctuate (e.g., 0.45V instead of 0.4375V).
        # The Guard Ring intercepts this wave and snaps it violently back onto your 
        # strict 0.0625V intervals before it is allowed to touch the PCIe bus.
        clean_hex_stream = self.rt_guard_ring.isolate_logic_stream(raw_electrical_stream)
        
        print(f"[RADIO RX] Extracted {len(clean_hex_stream)} secure hex states from atmospheric noise.")
        return clean_hex_stream
