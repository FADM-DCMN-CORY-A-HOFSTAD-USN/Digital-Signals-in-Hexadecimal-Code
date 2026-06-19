import json

# Load the master logic levels
with open('logic_levels.json', 'r') as file:
    hex_levels = json.load(file)

# Function to get the voltage for a specific hex character and scale
def get_voltage(hex_char, voltage_scale="1V"):
    scale_key = f"{voltage_scale}_logic"
    
    # Ensures the input is an uppercase string (e.g., 'a' becomes 'A')
    hex_char = str(hex_char).upper()
    
    return hex_levels[scale_key][hex_char]

# Example: The script needs to send Hex 'C' to the 1V circuit
target_voltage = get_voltage('C', '1V')
print(f"Injecting {target_voltage}V into the simulation.") 
# Output: Injecting 0.8125V into the simulation.
