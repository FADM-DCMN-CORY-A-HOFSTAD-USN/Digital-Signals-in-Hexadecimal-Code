from ..hex_rt_infrastructure import RTTraceRoute, RTGuardRing, RTPhaseChangeThermalInterface

class HexNativeLCD:
    """
    Native Hexadecimal Liquid Crystal Display (LCD-HX).
    Direct-drives pixel matrix using 0.0V-1.0V analog logic.
    Bypasses HDMI/DisplayPort digital encapsulation for zero-latency rendering.
    """
    def __init__(self, resolution_x=1024, resolution_y=768):
        self.res_x = resolution_x
        self.res_y = resolution_y
        self.total_pixels = self.res_x * self.res_y
        
        # RT Physical Infrastructure
        # Screens act as massive antennas for EM interference. The Guard Ring keeps the image perfectly static-free.
        self.rt_guard_ring = RTGuardRing()
        
        # Pushing millions of analog voltages at 60+ Hz requires heavy trace routing
        self.video_bus_trace = RTTraceRoute(copper_oz=1.5, trace_width_mm=2.0, length_mm=120.0)
        
        # The display controller IC gets incredibly hot processing direct analog frames
        self.rt_thermal_pad = RTPhaseChangeThermalInterface()
        self.thermal_state_c = 33.0

    def render_analog_frame(self, hex_rgb_matrix):
        """
        Takes a raw matrix of Hex-RGB analog states (0.0V - 1.0V) and directly 
        applies the voltage to the liquid crystal grid. 
        """
        print(f"\n[LCD-HX] Ingesting native analog frame ({self.res_x}x{self.res_y})...")
        
        # 1. Ensure the video bus can handle the current draw of the entire frame
        # Driving a full white screen (Hex F / 1.0V across all RGB subpixels) draws significant power
        safe_matrix, heat_w = self.video_bus_trace.transmit_analog_signal(current_amps=2.8, voltage_stream=hex_rgb_matrix)
        
        if not safe_matrix:
            print("[LCD-HX] FRAME DROP. Video trace impedance bottleneck detected.")
            return False
            
        # 2. Scrub the frame for motherboard crosstalk
        clean_frame = self.rt_guard_ring.isolate_logic_stream(safe_matrix)
        
        # 3. Direct-drive the crystals
        # A voltage of 1.0V (Hex F) fully opens the crystal for max brightness.
        # A voltage of 0.5V (Hex 8) opens it exactly halfway.
        # A voltage of 0.0V (Hex 0) leaves it shut (true black).
        print(f"[LCD-HX] Directly actuating {self.total_pixels * 3} liquid crystal subpixels.")
        
        # 4. Thermal Management
        self.thermal_state_c += heat_w * 0.3
        self.thermal_state_c = self.rt_thermal_pad.dissipate_heat(self.thermal_state_c, heat_w)
        
        print(f"[LCD-HX] Frame rendered successfully. Controller Temp: {self.thermal_state_c:.1f}°C")
        return True

    def hardware_diagnostics_overlay(self, pcie_bus_stream):
        """
        Bypasses the GPU entirely. Routes raw 16-state logic from the PCIe bus 
        directly to the glass for pure hardware-level visual diagnostics.
        """
        print("\n[LCD-HX] ENGAGING RAW HARDWARE OVERLAY...")
        
        clean_stream = self.rt_guard_ring.isolate_logic_stream(pcie_bus_stream)
        
        # Maps the raw 0.0625V intervals directly to a visual luminance scale on the screen
        print(f"[LCD-HX] Displaying {len(clean_stream)} raw PCIe voltage states directly on glass.")
        return True
