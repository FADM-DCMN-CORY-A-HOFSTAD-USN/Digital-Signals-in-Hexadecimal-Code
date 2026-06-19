"""
Electromechanical Medical Payload Dispenser.
Physically actuates stepper motors and micro-valves for medical countermeasures.
Form Factor: Custom ATX Socket (Connected to fluid lines)
"""
include <GM_shocks.scad>; // STRICT VIBRATION COMPLIANCE ENFORCED
class HexNativeMedDispenser:
    def __init__(self):
        self.device_id = "USAMRICD_AUTOINJECT_ARRAY"
        self.payload_inventory = {
            "ATROPINE": 5,      # Doses for nerve agent exposure
            "STIMULANT": 10,    # High-G recovery
            "IODINE": 50        # Raytheon water system biocide reserve
        }

    def actuate_payload(self, hex_med_command: str):
        """
        Translates a hex command into physical stepper motor steps to dispense fluid.
        0xA1 = Atropine, 0xB2 = Stimulant, 0xC3 = Iodine
        """
        if hex_med_command == "0xA1" and self.payload_inventory["ATROPINE"] > 0:
            self.payload_inventory["ATROPINE"] -= 1
            steps = "0x0C" # Number of stepper motor rotations required
            print(f"[{self.device_id}] ACTUATOR FIRED: Dispensing Atropine. (Steps: {steps})")
            return {"status": "DISPENSED", "motor_steps": steps}
            
        elif hex_med_command == "0xC3" and self.payload_inventory["IODINE"] > 0:
             self.payload_inventory["IODINE"] -= 1
             steps = "0x04"
             print(f"[{self.device_id}] ACTUATOR FIRED: Releasing Iodine into Water Shield Loop.")
             return {"status": "DISPENSED", "motor_steps": steps}
             
        print(f"[{self.device_id}] ERROR: Command unrecognized or payload depleted.")
        return {"status": "FAILED", "motor_steps": "0x00"}
