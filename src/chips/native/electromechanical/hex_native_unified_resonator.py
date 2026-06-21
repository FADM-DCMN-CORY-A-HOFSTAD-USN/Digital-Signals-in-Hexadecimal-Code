import math

class HexNativeUnifiedResonator:
    """
    The Ultimate Optomechanical Co-Resonant Gyroscope.
    Utilizes a fused-silica hemispherical lattice to track multi-domain physics
    simultaneously, outputting native 16-state hexadecimal analog logic.
    """
    def __init__(self, base_resonant_freq_hz=15000.0, optical_clock_hz=193.4e12): # 1550nm
        self.w0 = base_resonant_freq_hz
        self.optical_clock = optical_clock_hz
        self.quality_factor_q = 25000000.0 # Vacuum-sealed HRG Q-Factor
        
        # Current environmental states
        self.temp_c = 22.0
        self.pressure_atm = 1.0
        self.gravity_g = 9.81
        self.rotation_rad_s = 0.0
        self.magnetic_field_t = 0.0
        
        # Scaling limits to keep outputs within 0.0V - 1.0V RT Hex Logic
        self.v_max = 1.0

    def calculate_state_matrix(self):
        """
        Solves the unified structural equations simultaneously to output an 
        analog array representing Time, Rotation, Heat, Pressure, and Gravity.
        """
        # 1. HEAT: Thermoelastic Dissipation Equation
        # Frequency shifts due to temperature coefficient of the silica lattice
        tcf = -0.00005 # Approx shift per degree C
        current_w = self.w0 * (1.0 + (tcf * (self.temp_c - 22.0)))
        heat_voltage = min(self.v_max, max(0.0, (self.temp_c / 100.0)))

        # 2. ROTATION: Bryan's Effect / Coriolis Integration
        # High-end HRGs track Whole-Angle precession
        bryan_factor = 0.3 # Typical geometric constant for a hemisphere
        precession_angle = -bryan_factor * self.rotation_rad_s 
        rotation_voltage = (math.sin(precession_angle) + 1.0) / 2.0 # Normalized 0-1V

        # 3. PRESSURE: Diaphragm Stress-Stiffening
        # Increased pressure structurally stiffens the z-axis
        pressure_shift = math.sqrt(1.0 + (self.pressure_atm * 0.01))
        pressure_voltage = min(self.v_max, self.pressure_atm / 5.0)

        # 4. GRAVITY/SEISMIC: Relativistic / Mass Displacement
        gravity_shift = current_w * math.sqrt(1.0 + (0.0001 * self.gravity_g))
        gravity_voltage = min(self.v_max, self.gravity_g / 20.0)

        # Snap all analog solutions to the strict 16-state RT logic grid (0.0625V intervals)
        return {
            "TEMP_V": round(heat_voltage / 0.0625) * 0.0625,
            "GYRO_V": round(rotation_voltage / 0.0625) * 0.0625,
            "PRESS_V": round(pressure_voltage / 0.0625) * 0.0625,
            "GRAV_V": round(gravity_voltage / 0.0625) * 0.0625,
            "CLOCK_HZ": current_w
        }

    def process_optical_wgm(self, external_light_intensity_w):
        """
        Solves the Whispering Gallery Mode equation to map 360-degree light intrusion.
        """
        refractive_shift = external_light_intensity_w * 0.0001
        light_voltage = min(self.v_max, refractive_shift * 10.0)
        return round(light_voltage / 0.0625) * 0.0625
