import math

class HexNativeFlightCLAW:
    """
    Control Laws (CLAW) DSP Pipeline for the Saiya Class HOTAS.
    Bridges raw stick voltage to actual aerodynamic surface actuation natively.
    """
    def __init__(self):
        # Hotas Physics Profiles
        self.deadzone = 0.05
        self.curve = 0.25 # Cubic S-Curve magnitude
        self.saturation_limit = 0.95
        
        # Flight Envelope Constraints
        self.q_baseline = 101.3 # Reference dynamic pressure
        self.v_co = 150.0 # Crossover speed for C* pitch blending

    def execute_dsp_pipeline(self, raw_stick_v, v_center, current_dynamic_pressure_q):
        """
        Executes the mandatory 5-step Control Law pipeline documented for real aircraft.
        """
        print(f"\n[FLIGHT CLAW] Ingesting raw HOTAS axis voltage: {raw_stick_v}V")

        # 1. Polynomial Dewarping (Centering the physical Hall-Effect sensor)
        # Translates 0.0V-1.0V native range into a -1.0 to 1.0 logic vector
        normalized_x = (raw_stick_v - v_center) * 2.0 
        
        # 2. Deadzone Application (Eliminating stiction)
        if abs(normalized_x) < self.deadzone:
            x_dz = 0.0
            print("  -> [DSP] Inside deadzone. Nulling output.")
        else:
            # Rescale the remaining throw
            sign = 1.0 if normalized_x > 0 else -1.0
            x_dz = sign * ((abs(normalized_x) - self.deadzone) / (1.0 - self.deadzone))
            
        # 3. Cubic S-Curve Application
        # Output = X * |X| * Curve + X * (1 - Curve)
        x_curve = (x_dz * abs(x_dz) * self.curve) + (x_dz * (1.0 - self.curve))
        
        # 4. Saturation Limiting (Hardware Stops)
        x_sat = max(-self.saturation_limit, min(self.saturation_limit, x_curve))
        print(f"  -> [DSP] S-Curve applied. Filtered stick logic: {x_sat:.3f}")
        
        # 5. Dynamic Pressure Gain Scheduling
        # Reduces control surface sensitivity at extremely high Mach speeds
        gain_schedule = self.q_baseline / max(1.0, current_dynamic_pressure_q)
        actuator_command = x_sat * gain_schedule
        
        print(f"  -> [AERO] Gain Schedule (q={current_dynamic_pressure_q}): {gain_schedule:.2f}x")
        print(f"  -> [ACTUATOR] Final surface deflection command: {actuator_command:.3f}")
        
        return actuator_command

    def calculate_c_star_tracking(self, nz_g_load, pitch_rate_rad_s):
        """
        Calculates the C* (C-star) blending equation used in modern FBW transports.
        Blends Pitch Rate (low speed) with Normal G-Load (high speed).
        """
        c_star_feedback = nz_g_load + (self.v_co * pitch_rate_rad_s)
        return c_star_feedback
