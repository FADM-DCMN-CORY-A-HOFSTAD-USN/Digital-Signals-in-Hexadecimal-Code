import math
from ...hex_rt_infrastructure import RTGuardRing, RTTraceRoute, RTPhaseChangeThermalInterface

class HexNativeBipolarOscillator:
    """
    Native Hexadecimal Temporal Oscillator (Z-Series).
    Measures the subjective experience of time by tracking the physical 
    perimeter of an analog voltage oscillation around a solid-state bipolar axis.
    """
    def __init__(self, semi_major_axis_nm=500.0, semi_minor_axis_nm=480.0):
        # The Bipolar Axis dimensions (Elliptical boundary)
        self.semi_major = semi_major_axis_nm 
        self.semi_minor = semi_minor_axis_nm 
        
        # Bipolar Focal Distance Calculation
        self.focal_distance = math.sqrt(self.semi_major**2 - self.semi_minor**2)
        
        # RT Physical Infrastructure
        self.rt_guard_ring = RTGuardRing()
        
        # Twin parallel copper routing creating the two distinct poles of the oscillation
        self.alpha_pole_trace = RTTraceRoute(copper_oz=2.0, trace_width_mm=1.5, length_mm=10.0)
        self.beta_pole_trace = RTTraceRoute(copper_oz=2.0, trace_width_mm=1.5, length_mm=10.0)
        
        # Extreme oscillation velocities generate immense localized thermal friction
        self.rt_thermal_pad = RTPhaseChangeThermalInterface()
        self.thermal_state_c = 22.0

    def _calculate_oscillation_perimeter(self):
        """
        Uses Ramanujan's approximation for the exact perimeter of the bipolar boundary.
        Calculated via physical trace-geometry rather than software.
        """
        h = ((self.semi_major - self.semi_minor)**2) / ((self.semi_major + self.semi_minor)**2)
        perimeter = math.pi * (self.semi_major + self.semi_minor) * (1 + (3 * h) / (10 + math.sqrt(4 - 3 * h)))
        return perimeter

    def measure_relativistic_time_variance(self, analog_velocity_v):
        """
        Calculates the subjective experience of time.
        In this native architecture, velocity is represented purely by analog voltage amplitude.
        Hex F (1.0V) = c (Speed of Light limit within the crystalline medium).
        """
        print("\n[BIPOLAR OSCILLATOR] Energizing solid-state bipolar axis...")
        
        # Scrub the incoming analog velocity through the Guard Ring to prevent jitter
        clean_velocity = self.rt_guard_ring.isolate_logic_stream([analog_velocity_v])[0]
        
        # Fire the Alpha and Beta traces simultaneously to begin the bipolar orbit
        safe_a, heat_a = self.alpha_pole_trace.transmit_analog_signal(1.5, [clean_velocity])
        safe_b, heat_b = self.beta_pole_trace.transmit_analog_signal(1.5, [clean_velocity])
        
        if not (safe_a and safe_b):
            print("[BIPOLAR OSCILLATOR] FAULT: Trace impedance failed during bipolar split.")
            return False
            
        perimeter_nm = self._calculate_oscillation_perimeter()
        
        # Lorentz Factor / Time Dilation Hardware Math
        # clean_velocity (0.0 to 1.0) perfectly maps to v/c
        v_over_c_squared = clean_velocity ** 2
        
        # Protect against division-by-zero if pushing true Hex F (1.0V / c)
        if clean_velocity >= 0.9999:
            lorentz_factor = float('inf')
            print("[BIPOLAR OSCILLATOR] WARNING: Infinite time dilation achieved at boundary.")
        else:
            lorentz_factor = 1.0 / math.sqrt(1.0 - v_over_c_squared)
        
        # Subjective Time Variance calculation
        # The phase shift is measured and mapped directly to a 1V Hex state
        time_variance = clean_velocity * (lorentz_factor - 1.0)
        output_voltage = min(1.0, max(0.0, time_variance))
        
        # Snap the relativistic shift perfectly to the RT 16-state grid (0.0625V intervals)
        snapped_output = round(output_voltage / 0.0625) * 0.0625
        
        # Thermal cycle execution
        total_heat_w = heat_a + heat_b + (lorentz_factor * 0.1) 
        self.thermal_state_c += total_heat_w * 0.2
        self.thermal_state_c = self.rt_thermal_pad.dissipate_heat(self.thermal_state_c, total_heat_w)
        
        print(f"  -> [PHYSICS] Orbital Perimeter established: {perimeter_nm:.2f} nm.")
        print(f"  -> [PHYSICS] Lorentz Factor at {(clean_velocity*100):.1f}% c: {lorentz_factor:.4f}")
        print(f"  -> [OUTPUT] Temporal Variance mapped to native logic: {snapped_output}V.")
        
        return snapped_output
