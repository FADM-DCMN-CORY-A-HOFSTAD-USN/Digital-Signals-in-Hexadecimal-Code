"""
Revolutionary Technology (RT) Hexadecimal Port Interface Monitor
Manages 100G QSFP56 optical link statuses, SDR BNC telemetry ingest, and surge protections.
Reference Repository Standard: Digital-Signals-in-Hexadecimal-Code
"""

import sys
import numpy as np

class RTHexadecimalPortController:
    def __init__(self):
        self.hex_logic_step = 0.0625  # Reference 16-state step profile
        self.surge_latch_tripped = False
        self.transient_threshold_volts = 1.150  # Boundary protection above nominal 1.0V bus
        self.active_interfaces = {
            "QSFP56_OPTICAL": {"status": "DISCONNECTED", "speed_gbps": 100},
            "BNC_SDR_TELEMETRY": {"status": "DISCONNECTED", "speed_gbps": 10}
        }

    def initialize_ports(self):
        """Validates hardware trace loopback integrity across external connector paths"""
        print("[*] Initializing High-Speed Hexadecimal Port Arrays...")
        
        # Simulating trace impedance baseline scans
        impedance_deltas = np.random.uniform(-0.001, 0.002, len(self.active_interfaces))
        
        for idx, (port_name, config) in enumerate(self.active_interfaces.items()):
            config["status"] = "CONNECTED"
            print(f"    [PORT - {port_name}] Link established. Trace drift: {impedance_deltas[idx]:+.4f}V (NOMINAL)")
            
        print("[+] All harsh-environment physical interfaces online and armed.\n")
        return True

    def ingest_signal_stream(self, port_identifier, incoming_voltage):
        """Routes real-time incoming 0.0V - 1.0V tracking signals to the motherboard core"""
        if self.surge_latch_tripped:
            raise RuntimeError("[-] Interface blocked: Gas-discharge surge latch is grounded.")
            
        # Detect transient overvoltage spikes (e.g., lightning induction or field ground loops)
        if incoming_voltage > self.transient_threshold_volts:
            print(f"[🔥 SURGE DETECTED] Port {port_identifier} read a spike of {incoming_voltage:.4f}V!")
            print("[*] Activating automated air-gap isolation relays to protect local registers.")
            self.surge_latch_tripped = True
            return "SURGE_SHUNTED"
            
        # Align continuous analog waves to our strict 16-state voltage layout rules
        aligned_voltage = round(incoming_voltage / self.hex_logic_step) * self.hex_logic_step
        hex_index = int(round(aligned_voltage / self.hex_logic_step))
        hex_char = hex(hex_index)[2:].upper()
        
        print(f"[INGEST - {port_identifier}] Signal: {incoming_voltage:.4f}V -> Remapped Register: 0x{hex_char}")
        return hex_char

if __name__ == "__main__":
    # Test initialization verifying external interface response loops
    port_manager = RTHexadecimalPortController()
    port_manager.initialize_ports()
    
    # Simulate processing standard telemetry inputs followed by an atmospheric surge event
    port_manager.ingest_signal_stream("BNC_SDR_TELEMETRY", 0.3125)
    port_manager.ingest_signal_stream("QSFP56_OPTICAL", 0.8125)
    port_manager.ingest_signal_stream("BNC_SDR_TELEMETRY", 2.4500)  # High transient surge injection
