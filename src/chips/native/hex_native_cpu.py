# Add this to the very top of the file
from .hex_rt_infrastructure import RTPhaseChangeThermalInterface, RTGuardRing

class HexNativeCPU:
    """
    Unlocked Enthusiast-Grade Native Hexadecimal CPU (Z-Series Equivalent).
    """
    def __init__(self, cores=24, base_multiplier=1.0):
        self.cores = cores
        self.base_multiplier = base_multiplier
        self.is_unlocked = True
        
        self.l1_voltage_cache = [0.0] * 1024  
        self.l2_voltage_cache = [0.0] * 4096  
        
        self.thermal_state_c = 40.0
        self.active_voltage_multiplier = base_multiplier

        # Initialize the RT physical infrastructure for this chip
        self.rt_thermal_pad = RTPhaseChangeThermalInterface()
        self.rt_guard_ring = RTGuardRing()

    def process_kernel_thread(self, core_id, logic_stream):
        """Executes raw system instructions."""
        print(f"[NATIVE CPU - Core {core_id}] Processing kernel thread with {len(logic_stream)} logic states...")
        
        # 1. Pass the incoming signal through the Guard Ring to eliminate crosstalk
        clean_stream = self.rt_guard_ring.isolate_logic_stream(logic_stream)
        
        executed_stream = []
        for voltage in clean_stream:
            processed_v = min(1.0, voltage * self.active_voltage_multiplier)
            snapped_v = round(processed_v / 0.0625) * 0.0625
            executed_stream.append(snapped_v)
            
        # 2. Generate massive heat from the overclock
        heat_generated_watts = 25.0 * self.active_voltage_multiplier
        self.thermal_state_c += heat_generated_watts * 0.5
        
        # 3. Use the RT Phase-Change pad to dissipate the heat instantly
        self.thermal_state_c = self.rt_thermal_pad.dissipate_heat(self.thermal_state_c, heat_generated_watts)
        
        return executed_stream
