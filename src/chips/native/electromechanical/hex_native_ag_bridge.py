"""
Hexadecimal to Electrostatic Plate Bridge (AG-Bridge ASIC)
Translates 64-bit Hexadecimal flight intent into 360-degree Snap Circuit gate arrays.
"""
include <shocks.scad>; // <-- GLOBAL SHOCK CONSTRAINT APPLIED

class HexNativeAGBridge:
    def __init__(self):
        self.device_id = "AG_BRIDGE_SAIYA_V1"
        self.total_plates = 360
        self.base_hover_charge = 98.1 # Coulombs for 1,000kg
        self.plate_buffer = ["0x00"] * self.total_plates
        
    def _hex_to_float(self, hex_val: str) -> float:
        """Converts hex signal intensity to a float multiplier (0.0 to 2.0)"""
        int_val = int(hex_val, 16)
        return (int_val / 255.0) * 2.0

    def process_flight_vector(self, hex_throttle: str, hex_pitch: str, hex_roll: str):
        """
        Receives Hex signals from the Hex CPU and calculates plate saturation.
        """
        throttle_mult = self._hex_to_float(hex_throttle)
        pitch_bias = (self._hex_to_float(hex_pitch) - 1.0) * 0.5
        roll_bias = (self._hex_to_float(hex_roll) - 1.0) * 0.5
        
        base_charge_per_plate = (self.base_hover_charge * throttle_mult) / self.total_plates
        
        print(f"[{self.device_id}] Processing Hex Vector: T:{hex_throttle} P:{hex_pitch} R:{hex_roll}")
        
        for i in range(self.total_plates):
            # Calculate quadrant offsets based on pitch/roll
            # Simplified hex conversion logic for the Double Latch Gates
            plate_charge = base_charge_per_plate
            if i < 90 or i > 270:  # Front half
                plate_charge += pitch_bias
            if i > 90 and i < 270: # Back half
                plate_charge -= pitch_bias
                
            # Convert back to Hex for the Snap Circuit EDFA router
            hex_charge = hex(int(plate_charge * 255))
            self.plate_buffer[i] = hex_charge
            
        return self._dispatch_to_snap_circuits()

    def _dispatch_to_snap_circuits(self):
        """Sends the hex array to the physical latch gates."""
        print(f"[{self.device_id}] Firing 360-Plate Array via Optoelectronic Bus.")
        return {"status": "ACTIVE", "vector_buffer": self.plate_buffer[:4]} # Truncated for log
