from ..hex_rt_infrastructure import RTGuardRing, RTPhaseChangeThermalInterface
from .hex_rt_heatsink import RTVaporChamberHeatsink
from .electromechanical.hex_native_snap_circuit import CRIPSDoubleLatchGate
import math

class ArriLPLMountBridge:
    """
    ARRI LPL Large Format Cinema Mount.
    Required for 32K. Flange focal distance of 44mm with a massive 62mm throat 
    to prevent physical vignetting on the 65mm sensor.
    """
    def __init__(self):
        self.throat_diameter_mm = 62.0
        self.rt_guard_ring = RTGuardRing()
        self.current_t_stop = 2.0 # Cinema lenses use T-stops for pure light transmission
        
    def actuate_cinema_iris(self, target_t_stop):
        print(f"[LPL-MOUNT] Bridging hex logic to LPL contacts. Iris set to T/{target_t_stop}.")
        self.current_t_stop = target_t_stop

class HexNative32KQuantumSensor:
    """
    30720 x 17280 Large Format (65mm) Analogue Sensor.
    Pixels are so dense that capturing pure photon irradiance generates extreme thermal 
    friction. Features an active Thermoelectric (Peltier) Sub-Cooler.
    """
    def __init__(self):
        self.res_x = 30720
        self.res_y = 17280
        self.total_pixels = self.res_x * self.res_y
        
        # Thermodynamics: 530 million analog photodiodes firing simultaneously
        self.peltier_active = True
        self.sensor_surface_temp_c = 18.0 # Kept sub-ambient to prevent thermal noise
        
        # The sensor substrate is the CRIPS lattice itself
        self.quantum_backplane = CRIPSDoubleLatchGate(entanglement_id="LEVIATHAN_SENSOR_ARRAY")

    def capture_and_entangle(self, scene_radiance_l, aperture_t):
        """
        Maps real-world light to 1V analog states and instantly transmits 
        it across the entanglement lattice, bypassing copper traces.
        """
        # Irradiance physics mapping
        irradiance_et = (math.pi * scene_radiance_l) / (4 * (aperture_t ** 2))
        
        # Normalize to 0.0V - 1.0V strict RT Hex Grid
        base_voltage = min(1.0, max(0.0, irradiance_et / 100.0))
        hex_snapped_v = round(base_voltage / 0.0625) * 0.0625
        
        # Thermal Spike Calculation (Photon absorption friction)
        heat_spike_w = 120.0 
        if self.peltier_active:
            heat_spike_w *= 0.3 # Peltier aggressively nullifies the heat at the glass level
            
        print(f"[32K SENSOR] 530-Million point wavefront captured. Irradiance maps to {hex_snapped_v}V.")
        
        # ZERO CABLE TRANSMISSION: The sensor immediately shifts the macroscopic lattice
        self.quantum_backplane.entangle_state(hex_snapped_v)
        print(f"[32K SENSOR] Frame entangled to Storage Matrix. Zero copper transmission used.")
        
        return hex_snapped_v, heat_spike_w

class RT32KLeviathanCamera:
    """
    The RT-32K "Leviathan" Deep Space Cinema Rig.
    An uncompromised analogue monster.
    """
    def __init__(self):
        self.lens_mount = ArriLPLMountBridge()
        self.sensor = HexNative32KQuantumSensor()
        
        # Supreme Thermal Triad to handle the Peltier exhaust
        self.rt_thermal_pad = RTPhaseChangeThermalInterface()
        self.rt_vapor_chamber = RTVaporChamberHeatsink(thermal_capacity_watts=800.0)
        self.chassis_temp_c = 22.0
        
        # Ruggedization
        self.internal_elastomer_mounts = True
        self.vacuum_seal_integrity = 100.0

    def capture_32k_frame(self, scene_radiance):
        print("\n[LEVIATHAN] Initiating 32K Quantum Capture Sequence...")
        
        # 1. Lens Actuation
        self.lens_mount.actuate_cinema_iris(2.0)
        
        # 2. Photon Capture & Instant Entanglement
        frame_voltage, heat_generated = self.sensor.capture_and_entangle(scene_radiance, self.lens_mount.current_t_stop)
        
        # 3. Exhaust the massive heat from the Peltier cooler
        self.chassis_temp_c += (heat_generated * 0.2)
        self.chassis_temp_c = self.rt_thermal_pad.dissipate_heat(self.chassis_temp_c, heat_generated)
        self.chassis_temp_c = self.rt_vapor_chamber.execute_capillary_cycle(heat_generated, self.chassis_temp_c)
        
        print(f"[LEVIATHAN] 32K Frame secured. Chassis stabilized at {self.chassis_temp_c:.1f}°C.")
        return True
