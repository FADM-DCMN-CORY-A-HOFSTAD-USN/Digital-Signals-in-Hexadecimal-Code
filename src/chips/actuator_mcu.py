import json

class ElectromagneticActuatorMCU:
    """
    Microcontroller Unit designed to convert 16-state hexadecimal telemetry 
    into variable power output for electromagnetic coil actuators.
    """
    def __init__(self, logic_file_path='../src/logic_levels.json'):
        with open(logic_file_path, 'r') as file:
            self.logic_map = json.load(file)['1V_logic']
            
        # Maximum current draw (in Amps) for the Bitter-style coil winding
        self.max_coil_current = 150.0 

    def decode_telemetry(self, hex_signal_stream):
        """
        Processes an incoming array of hex signals and translates them 
        into magnetic force vectors.
        """
        print(f"[MCU] Processing {len(hex_signal_stream)} waypoint/telemetry vectors...")
        for i, hex_char in enumerate(hex_signal_stream):
            hex_char = str(hex_char).upper()
            if hex_char in self.logic_map:
                logic_voltage = self.logic_map[hex_char]
                
                # Scale the 0.0V - 1.0V logic into physical actuator current
                # Hex F (1.0V) = 100% current capacity
                actuator_draw = logic_voltage * self.max_coil_current
                
                print(f"  Vector {i}: Input {logic_voltage}V (Hex {hex_char}) -> Actuator Output: {actuator_draw:.2f}A")
            else:
                print(f"  Vector {i}: ERROR - Invalid Telemetry Hex '{hex_char}'")

# Example usage for testing
if __name__ == "__main__":
    mcu = ElectromagneticActuatorMCU()
    # Simulating a burst of incoming telemetry data
    telemetry_burst = ['0', '3', '7', 'A', 'F', 'D', '8']
    mcu.decode_telemetry(telemetry_burst)
