import json

class HexTensorALU:
    """
    Hexadecimal Arithmetic Logic Unit for Tensor/GPU processing.
    Computes mathematical operations by summing or modulating analog logic levels.
    """
    def __init__(self, logic_file_path='../src/logic_levels.json'):
        with open(logic_file_path, 'r') as file:
            self.logic_map = json.load(file)['1V_logic']
            # Reverse lookup: find Hex char by voltage
            self.voltage_to_hex = {v: k for k, v in self.logic_map.items()}

    def analog_add(self, voltage_a, voltage_b):
        """
        Simulates an analog summing amplifier circuit.
        If the voltage exceeds 1.0V (Hex F), it carries over the remainder.
        """
        raw_sum = voltage_a + voltage_b
        
        if raw_sum > 1.0:
            # Carry over logic (e.g., F + 1 = 10 in Hex)
            remainder_voltage = raw_sum - 1.0
            # Snap to nearest 0.0625V interval to simulate the physical LDO
            snapped_voltage = round(remainder_voltage / 0.0625) * 0.0625
            result_hex = self.voltage_to_hex.get(snapped_voltage, '0')
            return {"carry": 1, "voltage": snapped_voltage, "hex": result_hex}
        else:
            snapped_voltage = round(raw_sum / 0.0625) * 0.0625
            result_hex = self.voltage_to_hex.get(snapped_voltage, '0')
            return {"carry": 0, "voltage": snapped_voltage, "hex": result_hex}

# Example usage for testing
if __name__ == "__main__":
    alu = HexTensorALU()
    # Adding Hex 7 (0.5V) and Hex 4 (0.3125V)
    result = alu.analog_add(0.5, 0.3125)
    print(f"[ALU OP] 0.5V + 0.3125V = {result['voltage']}V (Hex {result['hex']}) Carry: {result['carry']}")
