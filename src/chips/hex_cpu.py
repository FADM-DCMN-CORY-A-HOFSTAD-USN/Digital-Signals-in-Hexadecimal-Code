class HexCPU:
    """Central Processing Unit built on 16-state logic gates."""
    def __init__(self, cores=8):
        self.cores = cores
        self.l1_cache = []

    def execute_instruction(self, hex_voltage_op_code):
        """Translates a specific voltage into a CPU instruction."""
        # e.g., 0.875V (Hex D) triggers a system interrupt
        if hex_voltage_op_code == 0.875:
            print("[CPU] Hardware Interrupt Triggered.")
        else:
            print(f"[CPU] Executing Hex Logic at {hex_voltage_op_code}V")

class HexAcceleratorCard:
    """
    Dedicated AI/Physics Accelerator. 
    Processes heavy matrix math for machine learning or aviation telemetry.
    """
    def __init__(self, type="AI_TENSOR"):
        self.type = type
        self.thermal_state_c = 35.0

    def receive_data(self, voltage_matrix):
        print(f"[ACCELERATOR - {self.type}] Ingesting matrix of {len(voltage_matrix)} Hex values for processing.")
        self.thermal_state_c += 2.5 # Simulating heat generation
        return [min(1.0, v + 0.0625) for v in voltage_matrix] # Dummy math operation
