class HexPowerSupply:
    """Main Digital PSU managing the XC6602 ultra-low dropout networks."""
    def __init__(self, total_wattage=1600):
        self.total_wattage = total_wattage
        self.active_draw = 0.0
        self.logic_rail_stability = 100.0 # Percentage

    def allocate_power(self, device_id, requested_watts):
        if self.active_draw + requested_watts <= self.total_wattage:
            self.active_draw += requested_watts
            return True
        else:
            print(f"[PSU ALERT] Over-current draw prevented on {device_id}. Protecting logic rail.")
            return False

class HexFanController:
    """Dynamic PWM fan controller driven by hexadecimal thermal states."""
    def __init__(self, fan_headers=6):
        self.fan_headers = fan_headers
        self.rpm_states = [0] * fan_headers

    def process_system_thermals(self, max_temp_c):
        """Spins up fans based on the hottest component in the system."""
        target_rpm = 0
        if max_temp_c > 85.0:
            target_rpm = 3000 # Emergency cooling
        elif max_temp_c > 60.0:
            target_rpm = 1500 # Active cooling
            
        self.rpm_states = [target_rpm] * self.fan_headers
        print(f"[THERMAL] Max system temp {max_temp_c}°C. All fans normalized to {target_rpm} RPM.")
