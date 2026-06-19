from ..hex_rt_infrastructure import RTPhaseChangeThermalInterface, RTGuardRing
class HexCPUCoprocessor:
    """
    Native CPU Math Coprocessor (FPU equivalent for Hex logic).
    """
    def __init__(self):
        self.status = "ONLINE"

    def execute_high_precision_math(self, baseline_voltage, logic_multiplier):
        """
        Takes a raw voltage and modulates it across the 16-state intervals.
        """
        print(f"[CPU ACCELERATOR] Modulating {baseline_voltage}V by hex factor {logic_multiplier}.")
        result = baseline_voltage * logic_multiplier
        # Snap to the nearest valid Hex state
        return round(result / 0.0625) * 0.0625
