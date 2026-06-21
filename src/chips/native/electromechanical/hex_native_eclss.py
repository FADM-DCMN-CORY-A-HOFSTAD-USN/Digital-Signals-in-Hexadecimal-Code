from ..hex_rt_infrastructure import RTGuardRing, RTTraceRoute, RTPhaseChangeThermalInterface

class HexNativeECLSS:
    """
    Native Hexadecimal Environmental Control and Life Support System (ECLSS-HX).
    Maintains cabin pressure, O2 scrubbing, and thermal limits for the Type-S Saiya Hull.
    Operates entirely on 1V analog logic, bypassing software latency for instantaneous corrections.
    """
    def __init__(self):
        self.rt_guard_ring = RTGuardRing()
        
        # Scrubbers and pumps require heavy current to operate physically
        self.pump_trace = RTTraceRoute(copper_oz=2.0, trace_width_mm=3.0, length_mm=45.0)
        self.rt_thermal_pad = RTPhaseChangeThermalInterface()
        self.thermal_state_c = 36.0
        
        # Baseline Analog Targets (16-State Hexadecimal)
        self.target_pressure_v = 1.0     # 1 ATM = Hex F (1.0V)
        self.target_o2_v = 0.625         # 21% O2 = Hex A (0.625V)
        self.critical_co2_v = 0.1875     # Dangerous CO2 = Hex 3 (0.1875V)

    def regulate_atmosphere(self, analog_sensor_stream):
        """
        Ingests real-time analog voltage from the cabin sensors.
        Automatically increases voltage to life-support pumps if levels deviate.
        """
        print("\n[ECLSS-HX] Scanning atmospheric telemetry matrix...")
        clean_stream = self.rt_guard_ring.isolate_logic_stream(analog_sensor_stream)
        
        pressure_v, o2_v, co2_v = clean_stream[0], clean_stream[1], clean_stream[2]
        pump_power_output = 0.0
        
        if pressure_v < self.target_pressure_v:
            print(f"[ECLSS-HX] WARNING: Cabin pressure dropping ({pressure_v}V). Spooling repressurization tanks.")
            pump_power_output = 1.0 # Max Power (Hex F)
            
        if co2_v >= self.critical_co2_v:
            print(f"[ECLSS-HX] WARNING: CO2 buildup detected. Overdriving carbon scrubbers.")
            pump_power_output = max(pump_power_output, 0.875) # Hex E
            
        if pump_power_output > 0.0:
            # Route the heavy voltage through the 2oz copper trace to the physical pumps
            safe_stream, heat_w = self.pump_trace.transmit_analog_signal(current_amps=4.5, voltage_stream=[pump_power_output])
            self.thermal_state_c = self.rt_thermal_pad.dissipate_heat(self.thermal_state_c, heat_w)
            
        return pump_power_output
