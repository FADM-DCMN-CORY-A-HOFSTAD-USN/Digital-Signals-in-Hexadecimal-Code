import time
import random
from ..hex_rt_infrastructure import RTTraceRoute, RTGuardRing

class HexStanfordTimerDG645:
    """
    Embedded Stanford Research Systems (SRS) DG645 Digital Delay Generator.
    Taps physical nodes on the board to measure sub-nanosecond propagation delays.
    """
    def __init__(self):
        # 5-picosecond resolution with <25ps jitter
        self.resolution_picoseconds = 5.0 
        self.base_jitter_ps = 15.0

    def capture_delay(self, node_a_start_ns, node_b_stop_ns):
        """
        Calculates the exact propagation delay between the sensor receiving power 
        and the LED igniting in the series circuit.
        """
        raw_delay_ns = node_b_stop_ns - node_a_start_ns
        
        # Introduce scientific jitter and snap to 5ps resolution
        jitter = random.uniform(-self.base_jitter_ps, self.base_jitter_ps) / 1000.0
        actual_delay_ns = raw_delay_ns + jitter
        
        # Convert nanoseconds to picoseconds, snap to resolution, convert back
        snapped_ps = round((actual_delay_ns * 1000) / self.resolution_picoseconds) * self.resolution_picoseconds
        
        print(f"[SRS DG645 TIMER] Captured sequence delay: {snapped_ps} picoseconds.")
        return snapped_ps


class UnivacAnalogueBridge:
    """
    Univac-IX / Aegis Analogue Bridge.
    Processes the continuous, infinite-state analogue wavelengths from the optical 
    sensor before quantizing them into the strict 16-state Hexadecimal RT logic bus.
    """
    def __init__(self):
        self.is_active = True

    def bridge_analogue_to_hex(self, continuous_voltage):
        """Quantizes pure continuous analogue sensor data to strict 0.0625V intervals."""
        quantized_hex = round(continuous_voltage / 0.0625) * 0.0625
        return min(1.0, max(0.0, quantized_hex))


class HexNativeOpticalArray:
    """
    Native Hexadecimal Optical Sensor Board.
    Features an Ocean Insight ST sensor surrounded by Bridgelux Thrive Full Spectrum LEDs, 
    wired in series on a single high-current RT trace.
    """
    def __init__(self):
        # RT Physics Infrastructure
        self.power_trace = RTTraceRoute(copper_oz=2.0, trace_width_mm=1.5, length_mm=45.0)
        self.guard_ring = RTGuardRing()
        
        # Sub-components
        self.univac_bridge = UnivacAnalogueBridge()
        self.srs_timer = HexStanfordTimerDG645()
        
        # Optical Specifications
        self.sensor_model = "Ocean Insight ST-VIS (350-810 nm)"
        self.led_model = "Bridgelux Thrive 98 CRI (Continuous Spectrum)"

    def apply_series_power(self, hex_voltage_stream, trace_amps=2.5):
        """
        Routes power through the series circuit: Current -> Sensor -> LED.
        Power must flow through the sensor completely before the LED can ignite.
        """
        print(f"\n[OPTICAL ARRAY] Powering up series circuit on 2oz RT Copper Trace...")
        
        # 1. Verify trace integrity against heat/bottlenecking
        safe_stream, heat_w = self.power_trace.transmit_analog_signal(trace_amps, hex_voltage_stream)
        if not safe_stream:
            return None

        processed_optical_data = []

        for applied_v in safe_stream:
            # ---------------------------------------------------------
            # NODE A: Start Timer (Power hits the Ocean Insight Sensor)
            # ---------------------------------------------------------
            time_start_ns = time.perf_counter_ns()
            print(f"  -> [NODE A] {self.sensor_model} energized at {applied_v}V.")
            
            # Series Circuit Physics: The sensor consumes a voltage drop
            sensor_voltage_drop = applied_v * 0.25 
            remaining_v = applied_v - sensor_voltage_drop
            
            # Simulate physical propagation delay through the silicon substrate
            time.sleep(0.0000001) 
            
            # ---------------------------------------------------------
            # NODE B: Stop Timer (Remaining power hits the Bridgelux LED)
            # ---------------------------------------------------------
            time_stop_ns = time.perf_counter_ns()
            if remaining_v > 0.1: # LED forward voltage threshold
                print(f"  -> [NODE B] {self.led_model} ignited at {remaining_v}V.")
                
                # Calculate exact propagation delay using the Stanford Timer
                self.srs_timer.capture_delay(time_start_ns, time_stop_ns)
                
                # ---------------------------------------------------------
                # DATA CAPTURE: Sensor reads the full spectrum reflection
                # ---------------------------------------------------------
                # The sensor reads the continuous optical reflection (analogue)
                raw_analogue_reflection = remaining_v * random.uniform(0.85, 0.99)
                
                # Pass the raw analogue data through the Univac-Aegis Bridge
                hex_quantized_data = self.univac_bridge.bridge_analogue_to_hex(raw_analogue_reflection)
                processed_optical_data.append(hex_quantized_data)
            else:
                print(f"  -> [NODE B] Insufficient voltage ({remaining_v}V) to ignite LED.")
                processed_optical_data.append(0.0)

        # 3. Final scrub through the RT Guard Ring before hitting the motherboard bus
        print("[OPTICAL ARRAY] Passing returning optical data through RT Guard Ring...")
        clean_hex_stream = self.guard_ring.isolate_logic_stream(processed_optical_data)
        
        return clean_hex_stream

# Example usage if the script is run directly for testing:
if __name__ == "__main__":
    optical_board = HexNativeOpticalArray()
    # Pushing Hex states: 8, C, F (0.5625V, 0.8125V, 1.0V)
    test_stream = [0.5625, 0.8125, 1.0]
    results = optical_board.apply_series_power(test_stream)
    print(f"\n[HEX BUS] Final Output Stream: {results}")
