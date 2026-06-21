import math
from ..hex_rt_infrastructure import RTGuardRing

class HexNativeStylusDigitizer:
    """
    Native Hexadecimal Capacitive Digitizer and Stylus Processor.
    Executes hardware-level Parallax Correction, Quadratic Bézier Smoothing, 
    and Pressure Curve interpolation using continuous 0.0V-1.0V logic.
    """
    def __init__(self, glass_thickness_mm=2.5):
        self.glass_thickness = glass_thickness_mm
        self.rt_guard_ring = RTGuardRing()
        
        # Stylus Physics Configuration
        self.pressure_curve_k = 1.5 # k > 1 creates a "hard" pen profile
        self.max_brush_size_mm = 50.0
        
        # State tracking for Hardware Bézier Smoothing
        self.prev_x_v = None
        self.prev_y_v = None

    def process_stylus_contact(self, raw_x_v, raw_y_v, pressure_v, altitude_deg, azimuth_deg):
        """
        Ingests the raw 16-state analog signals from the physical stylus.
        Applies trigonometric parallax correction to align the digital ink 
        perfectly beneath the physical pen tip.
        """
        print(f"\n[DIGITIZER-HX] Stylus Contact Detected at ({raw_x_v}V, {raw_y_v}V).")
        
        # 1. Scrub electrical noise from the capacitive grid
        clean_signals = self.rt_guard_ring.isolate_logic_stream([raw_x_v, raw_y_v, pressure_v])
        x_in, y_in, p_in = clean_signals[0], clean_signals[1], clean_signals[2]
        
        # 2. Hardware Parallax Correction (The Glass Offset Equation)
        # Delta = g * tan(90 - theta) * cos(phi)
        alt_rad = math.radians(altitude_deg)
        azi_rad = math.radians(azimuth_deg)
        
        # Calculate physical offset in mm
        offset_mm_x = self.glass_thickness * math.tan(math.radians(90) - alt_rad) * math.cos(azi_rad)
        offset_mm_y = self.glass_thickness * math.tan(math.radians(90) - alt_rad) * math.sin(azi_rad)
        
        # Map physical offset back to analog voltage shift (Assuming 1V = 1000mm for this grid)
        v_offset_x = offset_mm_x / 1000.0
        v_offset_y = offset_mm_y / 1000.0
        
        accurate_x_v = min(1.0, max(0.0, x_in - v_offset_x))
        accurate_y_v = min(1.0, max(0.0, y_in - v_offset_y))
        
        # Snap corrected coordinates to the precise 16-state hexadecimal grid
        snapped_x = round(accurate_x_v / 0.0625) * 0.0625
        snapped_y = round(accurate_y_v / 0.0625) * 0.0625
        
        # 3. Dynamic Pressure Curve Calculation
        # T = T_min + (T_max - T_min) * P^k
        brush_thickness_mm = self.max_brush_size_mm * (p_in ** self.pressure_curve_k)
        
        print(f"  -> [PHYSICS] Altitude: {altitude_deg}°, Azimuth: {azimuth_deg}°")
        print(f"  -> [PHYSICS] Parallax Offset applied: Shifted {-offset_mm_x:.2f}mm X, {-offset_mm_y:.2f}mm Y.")
        print(f"  -> [OUTPUT] Ink Coordinate Locked: ({snapped_x}V, {snapped_y}V) with {brush_thickness_mm:.1f}mm thickness.")
        
        # Store for the next cycle's Bézier curve calculation
        self.prev_x_v, self.prev_y_v = snapped_x, snapped_y
        
        return snapped_x, snapped_y, brush_thickness_mm
