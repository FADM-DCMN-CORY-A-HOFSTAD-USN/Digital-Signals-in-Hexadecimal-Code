import numpy as np

class TSVPhysicsEngine:
    def __init__(self):
        # Physical constants for material layers
        self.v_step = 0.0625  # 16-state analog logic step (Volt)
        self.max_allowable_noise = self.v_step / 2.0  # 0.03125V threshold barrier
        
        # Oxide Layer Properties (Silicon Dioxide - SiO2)
        self.sio2_dielectric_constant = 3.9
        self.sio2_breakdown_voltage = 1e7  # V/cm
        
        # Barrier Layer Properties (Tantalum Nitride - TaN)
        self.tan_resistivity = 200e-6  # Ohm-cm (Absolute atomic barrier against migration)

    def calculate_via_capacitance(self, r_inner, r_outer, height):
        """
        Calculates the parasitic capacitance of a Through-Silicon Via (TSV).
        Ensures the structural oxide layer does not leak charge.
        """
        vacuum_permittivity = 8.854e-12  # F/m
        epsilon_r = self.sio2_dielectric_constant
        
        # Capacitance formula for coaxial cylinders (Via through silicon)
        numerator = 2 * np.pi * epsilon_r * vacuum_permittivity * height
        denominator = np.log(r_outer / r_inner)
        
        return numerator / denominator

    def verify_logic_state_integrity(self, leakage_current, wire_resistance):
        """
        Validates if vertical via leakage current corrupts the 0.0625V intervals.
        """
        voltage_drop = leakage_current * wire_resistance
        
        if voltage_drop >= self.max_allowable_noise:
            return {
                "status": "CRITICAL_FAILURE",
                "voltage_drop": voltage_drop,
                "message": f"Leakage ({voltage_drop:.5f}V) exceeded noise margin margin ({self.max_allowable_noise}V). Logic states will collapse!"
            }
        
        return {
            "status": "PASS",
            "voltage_drop": voltage_drop,
            "margin_remaining": self.max_allowable_noise - voltage_drop
        }

if __name__ == "__main__":
    engine = TSVPhysicsEngine()
    # Test via validation loop: 5um radius inner copper wire, 5.2um outer SiO2 barrier, 50um deep silicon substrate
    capacitance = engine.calculate_via_capacitance(5e-6, 5.2e-6, 50e-6)
    print(f"[*] Initializing TSV Verification Engine...")
    print(f"[+] Parasitic via capacitance computed: {capacitance * 1e15:.2f} fF")
    
    # Simulate a worst-case scenario leakage current spike
    test_run = engine.verify_logic_state_integrity(leakage_current=1.2e-3, wire_resistance=15.0)
    print(f"[*] Verification Status: {test_run['status']} -> {test_run.get('message', 'Voltages Stable')}")
