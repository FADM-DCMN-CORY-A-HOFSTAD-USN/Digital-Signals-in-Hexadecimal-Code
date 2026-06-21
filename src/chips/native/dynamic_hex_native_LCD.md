from ..hex_rt_infrastructure import RTTraceRoute, RTGuardRing, RTPhaseChangeThermalInterface
import math

class HexNativeFreeformLCD:
    """
    Native Hexadecimal Freeform LCD Controller (LCD-HX v2.0).
    Supports standard VESA templates, custom resolutions, and physically 
    masked custom shapes (Circular, Hexagonal, Arbitrary) to reduce analog power draw.
    """
    
    # Pre-certified RT Display Templates
    TEMPLATES = {
        "UNIVAC_TERMINAL": {"x": 800, "y": 600, "shape": "RECTANGLE"},
        "FHD_1080P": {"x": 1920, "y": 1080, "shape": "RECTANGLE"},
        "4K_UHD": {"x": 3840, "y": 2160, "shape": "RECTANGLE"},
        "AVIONICS_RADAR": {"x": 1024, "y": 1024, "shape": "CIRCLE"},     # Round display
        "ROBOTICS_EYE": {"x": 512, "y": 512, "shape": "HEXAGON"}         # Hexagonal cutout
    }

    def __init__(self, template_name=None, custom_x=None, custom_y=None, custom_shape="RECTANGLE"):
        # 1. Resolution & Geometry Resolution
        if template_name and template_name in self.TEMPLATES:
            config = self.TEMPLATES[template_name]
            self.res_x, self.res_y = config["x"], config["y"]
            self.shape = config["shape"]
        else:
            self.res_x = custom_x or 1024
            self.res_y = custom_y or 768
            self.shape = custom_shape

        # 2. Generate the Physical Hardware Mask
        self.pixel_mask = self._generate_hardware_mask()
        self.active_pixel_count = sum(sum(row) for row in self.pixel_mask)
        
        print(f"\n[LCD-HX FREEFORM] Initialized {self.shape} layout at {self.res_x}x{self.res_y}.")
        print(f"  -> Bounding Box: {self.res_x * self.res_y} pixels.")
        print(f"  -> Active Glass: {self.active_pixel_count} pixels ({(self.active_pixel_count/(self.res_x*self.res_y))*100:.1f}% material usage).")

        # 3. RT Physical Infrastructure
        self.rt_guard_ring = RTGuardRing()
        self.rt_thermal_pad = RTPhaseChangeThermalInterface()
        
        # We scale the trace copper based on the *active* pixel count, not the bounding box
        trace_amps_required = (self.active_pixel_count / 1000000) * 1.5
        self.video_bus_trace = RTTraceRoute(copper_oz=2.0, trace_width_mm=2.5, length_mm=100.0)
        self.thermal_state_c = 34.0

    def _generate_hardware_mask(self):
        """
        Creates a 2D boolean array. True = Liquid crystal exists at this coordinate.
        False = Glass was cut away; routing power here will cause an electrical short.
        """
        mask = []
        center_x, center_y = self.res_x / 2.0, self.res_y / 2.0
        
        for y in range(self.res_y):
            row = []
            for x in range(self.res_x):
                if self.shape == "CIRCLE":
                    # Cut away glass outside the radius
                    radius = min(center_x, center_y)
                    if (x - center_x)**2 + (y - center_y)**2 <= radius**2:
                        row.append(True)
                    else:
                        row.append(False)
                elif self.shape == "HEXAGON":
                    # Simplified hexagonal bounding math
                    dx, dy = abs(x - center_x) / center_x, abs(y - center_y) / center_y
                    if dx + dy <= 1.5 and dx <= 1.0 and dy <= 1.0:
                        row.append(True)
                    else:
                        row.append(False)
                else:
                    # Default Rectangle
                    row.append(True)
            mask.append(row)
        return mask

    def render_analog_frame(self, raw_hex_matrix):
        """
        Actuates the liquid crystals based on the analog matrix, strictly adhering 
        to the hardware mask to prevent power loss in dead zones.
        """
        # Scrub frame via Guard Ring
        clean_matrix = self.rt_guard_ring.isolate_logic_stream(raw_hex_matrix)
        
        # Calculate dynamic power draw based ONLY on crystals that actually exist
        total_voltage_draw = 0.0
        idx = 0
        
        for y in range(self.res_y):
            for x in range(self.res_x):
                if self.pixel_mask[y][x]:
                    # Physical crystal exists here. Draw power to twist it.
                    if idx < len(clean_matrix):
                        total_voltage_draw += clean_matrix[idx]
                idx += 3  # Advance by 3 (R, G, B subpixels)

        # Transmit the highly-specific analog power load through the RT trace
        dynamic_amps = (total_voltage_draw / self.active_pixel_count) * 2.8
        safe_stream, heat_w = self.video_bus_trace.transmit_analog_signal(dynamic_amps, [1.0])
        
        if safe_stream:
            self.thermal_state_c += heat_w * 0.2
            self.thermal_state_c = self.rt_thermal_pad.dissipate_heat(self.thermal_state_c, heat_w)
            return True
            
        print("[LCD-HX FREEFORM] FRAME DROP. Trace impedance failed under custom shape load.")
        return False
