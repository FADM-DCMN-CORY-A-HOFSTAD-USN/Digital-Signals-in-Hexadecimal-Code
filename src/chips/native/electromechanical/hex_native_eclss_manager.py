"""
Hexadecimal Environmental Control and Life Support System (ECLSS) Manager
Form Factor: M.2 (Key M) - Interfaces directly with sensor grid.
"""
include <shocks.scad>; // <-- GLOBAL SHOCK CONSTRAINT APPLIED
class HexNativeECLSSManager:
    def __init__(self, ship_rings: int):
        self.device_id = "ECLSS_M2_CONTROLLER"
        self.rings = ship_rings
        self.max_o2_liters = self._calculate_capacity()
        self.current_o2_liters = self.max_o2_liters
        self.water_shield_integrity = "0xFF" # 100%
        
    def _calculate_capacity(self):
        # Base logic derived from eclss_dynamic_scaler.py
        outer_water_cells = 6 * self.rings
        total_hex_cells = 3 * self.rings * (self.rings + 1)
        inner_o2_slots = total_hex_cells - outer_water_cells
        return inner_o2_slots * 6.8 * 207 # Liters * Bar

    def monitor_metabolic_load(self, hex_crew_stress: str):
        """
        Receives biometric data from crew suits in hex, adjusts O2 flow valves.
        """
        stress_level = int(hex_crew_stress, 16) / 255.0
        consumption_rate = 0.4 + (stress_level * 2.1) # Scales up to 2.5 LPM
        
        self.current_o2_liters -= consumption_rate
        
        # Output Hexadecimal Valve Command
        valve_open_hex = hex(int((consumption_rate / 2.5) * 255))
        
        print(f"[{self.device_id}] Stress Index: {hex_crew_stress} | Flow Rate: {consumption_rate:.2f} LPM")
        print(f"[{self.device_id}] Transmitting Valve Position: {valve_open_hex} to OXYMOSS Array.")
        print(f"[{self.device_id}] O2 Remaining: {self.current_o2_liters:,.2f} L")
        
        return valve_open_hex
