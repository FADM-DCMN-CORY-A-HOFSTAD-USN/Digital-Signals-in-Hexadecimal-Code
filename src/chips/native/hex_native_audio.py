from ..hex_rt_infrastructure import RTTraceRoute, RTGuardRing, RTPhaseChangeThermalInterface

class HexNativeAudioDSP:
    """
    Native Hexadecimal Audio Digital Signal Processor (DSP-HX).
    Bypasses standard binary DACs. Amplifies 16-state RT logic directly 
    into physical acoustic waveforms, or ingests raw microphone data 
    for acoustic forensic analysis.
    """
    def __init__(self, channels="7.1_Surround"):
        self.channels = channels
        
        # Audio traces are highly susceptible to electromagnetic interference (EMI).
        # The Guard Ring acts as a Faraday cage to prevent GPU/CPU noise from creating audible hiss.
        self.rt_guard_ring = RTGuardRing()
        self.rt_thermal_pad = RTPhaseChangeThermalInterface()
        
        # Driving physical speaker coils (especially subwoofers) requires massive current.
        # We enforce an ultra-thick 3.0mm, 2oz copper RT trace to prevent the amplifier from melting.
        self.amplifier_trace = RTTraceRoute(copper_oz=2.0, trace_width_mm=3.0, length_mm=40.0)
        self.thermal_state_c = 38.0

    def synthesize_telemetry_audio(self, hex_voltage_stream, volume_gain_multiplier=25.0):
        """
        Takes a stream of native 16-state logic from the PCIe bus and 
        amplifies it directly into a physical speaker coil.
        """
        print(f"\n[NATIVE AUDIO DSP] Routing {len(hex_voltage_stream)} hex states to Class-A amplifier stages...")
        
        # 1. Scrub the incoming signal of any PCIe bus jitter
        clean_audio_stream = self.rt_guard_ring.isolate_logic_stream(hex_voltage_stream)
        
        # 2. Amplify the 1.0V max logic up to speaker-level voltage
        # Example: Hex F (1.0V) * 25.0 Gain = 25.0V output to the speaker cone
        amplified_waveform = [v * volume_gain_multiplier for v in clean_audio_stream]
        
        # 3. Push the heavy current through the 2oz copper RT trace
        # A 25V signal driving a standard 8-ohm speaker draws roughly 3.1 Amps
        safe_stream, heat_w = self.amplifier_trace.transmit_analog_signal(current_amps=3.1, voltage_stream=amplified_waveform)
        
        if safe_stream:
            # 4. Handle extreme amplifier heat dump
            self.thermal_state_c += heat_w * 0.4
            self.thermal_state_c = self.rt_thermal_pad.dissipate_heat(self.thermal_state_c, heat_w)
            
            print(f"[NATIVE AUDIO DSP] Acoustic wave synthesized perfectly. Thermal state: {self.thermal_state_c:.1f}°C.")
            return safe_stream
        else:
            print("[NATIVE AUDIO DSP] AMPLIFIER FAULT. Trace bottleneck detected under heavy acoustic load.")
            return None

    def ingest_acoustic_forensics(self, raw_microphone_voltage):
        """
        Takes continuous, infinite-resolution physical sound waves from a laboratory 
        microphone and quantizes them down into the strict 16-state RT logic grid.
        """
        print("\n[NATIVE AUDIO DSP] Ingesting continuous acoustic wave from microphone...")
        
        quantized_hex_stream = []
        for v in raw_microphone_voltage:
            # The preamp scales the mic signal to 0.0V-1.0V, then we snap it 
            # to the exact 0.0625V intervals required by the Z-Series CPU.
            snapped_v = round(min(1.0, max(0.0, v)) / 0.0625) * 0.0625
            quantized_hex_stream.append(snapped_v)
            
        print(f"[NATIVE AUDIO DSP] Acoustic data quantized to 16-state RT logic. Ready for PCIe bus.")
        return quantized_hex_stream
