from ..hex_rt_infrastructure import RTGuardRing, RTTraceRoute, RTPhaseChangeThermalInterface
from .hex_gpu_accelerator import HexNativeGPU
from .hex_native_cpu import HexNativeCPU
from .hex_native_ssd import HexNativeSSD
from .electromechanical.hex_native_snap_circuit import CRIPSDoubleLatchGate
import math

class CanonEFMountBridge:
    """
    Translates legacy binary Canon EF lens communication into native RT Hex logic.
    Provides analogue voltage control over the internal focus motors and iris blades.
    """
    def __init__(self):
        self.pins = ["VDD", "VSS", "DCL", "DLC", "LCLK", "D-OUT", "D-IN"]
        self.rt_guard_ring = RTGuardRing()
        self.current_aperture_f = 2.8
        
    def actuate_iris(self, target_f_stop):
        print(f"[EF-MOUNT] Bridging hex logic to EF pinout. Actuating iris to f/{target_f_stop}...")
        self.current_aperture_f = target_f_stop
        return True

class HexNative16KSensor:
    """
    15360 x 8640 Full-Spectrum Analogue Sensor (200nm UV to 1000nm NIR).
    Applies the Pinhole & Image Plane Irradiance equations directly to hardware voltage.
    """
    def __init__(self):
        self.res_x = 15360
        self.res_y = 8640
        self.pixel_pitch_um = 3.125
        self.nyquist_freq = 160.0 # lp/mm
        self.active_frame_matrix = []

    def capture_photons_to_voltage(self, scene_radiance_l, aperture_n):
        """
        Maps real-world lighting to 1V analog intervals using the Camera Equation:
        E_t = (pi * L_s) / (4 * N^2)
        """
        irradiance_et = (math.pi * scene_radiance_l) / (4 * (aperture_n ** 2))
        
        # Normalize to 0.0V - 1.0V strict RT Hex Grid
        base_voltage = min(1.0, max(0.0, irradiance_et / 100.0))
        hex_snapped_v = round(base_voltage / 0.0625) * 0.0625
        
        print(f"[16K SENSOR] Full-Spectrum wavefront captured. Base irradiance maps to {hex_snapped_v}V.")
        return hex_snapped_v

class RT16KMonolithCamera:
    """
    The Ultimate Analogue Cinema Rig.
    Integrated CPU, CUDA, memory, rugged isolation, and quantum entanglement M.2.
    """
    def __init__(self):
        # --- OPTICS ---
        self.lens_mount = CanonEFMountBridge()
        self.sensor = HexNative16KSensor()
        
        # --- COMPUTE & STORAGE ---
        self.cpu = HexNativeCPU(cores=8)
        self.gpu_cuda = HexNativeGPU(tensor_cores=2048) # Handles MTF and 3D depth tracking natively
        self.internal_storage = HexNativeSSD(capacity_tb=32)
        
        # The M.2 Quantum Ansible Expansion (CRIPS Double Latch)
        self.m2_snap_slot = CRIPSDoubleLatchGate(entanglement_id="MONOLITH_CAM_1")
        
        # --- I/O & POWER ---
        # Legacy USB 3.2 Gen 2 Bridge (10Gbps Digital translation for commercial PC offloading)
        self.usb_3_bridge = RTTraceRoute(copper_oz=1.5, trace_width_mm=1.0, length_mm=20.0)
        self.battery_cell = 100.0 # Solid-State Lithium-Ceramic (150Wh)
        
        # --- RUGGEDIZATION ---
        self.internal_elastomer_mounts_intact = True
        self.waterproof_seal_integrity = 100.0

    def execute_cinematic_capture(self, scene_radiance, focal_distance_mm):
        """Processes a single 16K frame directly into the analogue SSD and GPU."""
        if not self.internal_elastomer_mounts_intact:
            print("[MONOLITH ERROR] Vibration isolators sheared. Sensor alignment failed.")
            return False
            
        print("\n[MONOLITH] Initiating 16K Analogue Frame Capture...")
        
        # 1. Lens Communication
        self.lens_mount.actuate_iris(2.8)
        
        # 2. Photon Capture
        frame_voltage = self.sensor.capture_photons_to_voltage(scene_radiance, self.lens_mount.current_aperture_f)
        
        # 3. CUDA Depth/Epipolar Processing
        print("[CUDA] Processing stereo/disparity vectors for 3D depth tracking...")
        # Simulating the GPU running the epipolar matrix Z = (f * B) / d
        depth_map = frame_voltage * 0.5 
        
        # 4. Storage & Entanglement
        self.internal_storage.write_analog_block([frame_voltage, depth_map])
        
        # Beam the frame instantly to the ship via the M.2 Snap Circuit
        self.m2_snap_slot.entangle_state(frame_voltage)
        
        # Power drain
        self.battery_cell -= 0.05
        print(f"[MONOLITH] Frame secured. Battery at {self.battery_cell:.1f}%.")
        return True
