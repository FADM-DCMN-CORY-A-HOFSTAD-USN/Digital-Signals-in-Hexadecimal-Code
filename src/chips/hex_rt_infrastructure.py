import math

class RTPhaseChangeThermalInterface:
    """
    Simulates advanced Revolutionary Technology Phase Change Material (RT-PCM).
    Outlasts traditional thermal paste by liquefying under heavy analog logic loads to eliminate pump-out.
    """
    def __init__(self):
        self.is_liquid = False
        self.thermal_conductivity = 0.8  # Solid state conductivity
        self.activation_temp_c = 45.0

    def dissipate_heat(self, current_temp_c, heat_load_watts):
        # The pad is completely solid at room temperature. Once the chip crosses 45C, 
        # the RT pad liquefies into a micro-thin layer, drastically increasing heat transfer.
        if current_temp_c >= self.activation_temp_c and not self.is_liquid:
            self.is_liquid = True
            self.thermal_conductivity = 8.5  # Liquefied state (massive cooling spike)
            print(f"[RT THERMAL] Component hit {current_temp_c}°C. RT-PCM pad liquefied. Max cooling engaged.")
        
        elif current_temp_c < self.activation_temp_c - 5.0 and self.is_liquid:
            self.is_liquid = False
            self.thermal_conductivity = 0.8
            print("[RT THERMAL] Load dropped. RT-PCM pad contracted to solid state.")

        # Calculate temperature drop based on active conductivity
        temp_reduction = (self.thermal_conductivity * 2.5) - (heat_load_watts * 0.1)
        return max(30.0, current_temp_c - temp_reduction)


class RTTraceRoute:
    """
    RT proprietary trace routing logic based on Joule's First Law and geometric trace laws.
    Enforces thick, 2oz copper pathways to eliminate resistance bottlenecks for high-draw logic.
    """
    def __init__(self, copper_oz=2.0, trace_width_mm=1.5, length_mm=50.0):
        self.copper_oz = copper_oz
        self.cross_sectional_area = copper_oz * trace_width_mm
        
        # R = rho * (L/A). Thicker RT traces (High A) drastically lower Resistance (R).
        self.electrical_resistance = (0.017 * length_mm) / self.cross_sectional_area
        
    def transmit_analog_signal(self, current_amps, voltage_stream):
        """
        Calculates thermal bottlenecks. P = I^2 * R.
        If the current is massive and the trace is thin, it generates lethal heat.
        """
        heat_generated_watts = (current_amps ** 2) * self.electrical_resistance
        
        if heat_generated_watts > 15.0:
            print(f"[RT HARDWARE FAILURE] Trace melted. {heat_generated_watts:.1f}W heat dumped. Ensure RT 2oz standards are met.")
            return None, heat_generated_watts
            
        return voltage_stream, heat_generated_watts


class RTGuardRing:
    """
    An unbroken continuous trace of pure ground copper wrapped around critical silicon.
    Neutralizes stray electromagnetic noise before it corrupts the 16-state logic intervals.
    """
    def __init__(self):
        self.is_active = True

    def isolate_logic_stream(self, raw_voltage_stream):
        """
        Acts as an electronic moat. Any voltage fluctuating off the strict 
        0.0625V intervals (due to crosstalk) is intercepted and grounded by the RT ring.
        """
        isolated_stream = []
        for v in raw_voltage_stream:
            # The RT Guard Ring snaps the stray voltage back to perfect structural alignment
            perfect_v = round(v / 0.0625) * 0.0625
            
            if perfect_v != v:
                 # Stray noise hit the ring and was neutralized
                 v = perfect_v 
                 
            isolated_stream.append(v)
        return isolated_stream


class RevolutionaryZSeriesMotherboard:
    """
    The ultimate Revolutionary Technology (RT) certified physical substrate.
    Enforces 45-degree trace angles, multi-layer vias, and RT Guard Ring isolation.
    """
    def __init__(self):
        self.layers = 8 # Thick multi-layered PCB for structural integrity
        self.guard_ring = RTGuardRing()
        self.thermal_pad = RTPhaseChangeThermalInterface()
        self.ambient_temp_c = 35.0

    def route_via_thermal_drop(self, source_component, target_component, voltage_stream):
        """
        When a high-power RT trace hits a crowded area, it uses thermal micro-vias 
        to dive to the opposite side of the PCB, strictly enforcing the zero-cross rule.
        """
        print(f"[RT PCB ROUTING] High-speed data line approaching {target_component} power plane...")
        print("  -> Diving through micro-via to bottom layer.")
        print("  -> Routing cleanly underneath bottleneck.")
        print("  -> Surfacing at target pin.")
        
        # Pass the signal through the RT Guard Ring to eliminate any layer-hopping crosstalk
        clean_stream = self.guard_ring.isolate_logic_stream(voltage_stream)
        return clean_stream

    def route_45_degree_wrap(self, voltage_stream):
        """
        Wraps the lead around smoothly at a 45-degree angle. 
        Sharp 90-degree corners create electrical traffic jams (impedance spikes).
        """
        print("[RT PCB ROUTING] Applying 45-degree wrap-around routing to prevent high-frequency reflection.")
        # Signal speed remains uniform across the RT bus
        return voltage_stream
