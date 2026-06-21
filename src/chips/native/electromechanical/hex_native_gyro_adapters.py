from .hex_native_unified_resonator import HexNativeUnifiedResonator
from ...hex_rt_infrastructure import RTTraceRoute, RTGuardRing

class _BaseGyroHardware:
    def __init__(self):
        self.resonator = HexNativeUnifiedResonator()
        self.rt_guard_ring = RTGuardRing()

class Gyroscope_PCIe(_BaseGyroHardware):
    """
    PCIe x4 Gyroscope Array.
    Used for high-speed tensor AI robotics where latency must be zero.
    Requires heavy 2oz copper routing.
    """
    def __init__(self):
        super().__init__()
        self.bus_trace = RTTraceRoute(copper_oz=2.0, trace_width_mm=3.0, length_mm=60.0)

    def stream_telemetry(self):
        raw_matrix = self.resonator.calculate_state_matrix()
        # PCIe can blast all 4 analog voltages down the bus simultaneously
        payload = [raw_matrix["GYRO_V"], raw_matrix["TEMP_V"], raw_matrix["PRESS_V"], raw_matrix["GRAV_V"]]
        clean_payload = self.rt_guard_ring.isolate_logic_stream(payload)
        return self.bus_trace.transmit_analog_signal(1.5, clean_payload)[0]

class Gyroscope_M2(_BaseGyroHardware):
    """
    M.2 Form Factor Gyroscope.
    Compact planar mounting. Perfect for drones or the Type-S Saiya Hull avionics deck.
    """
    def __init__(self):
        super().__init__()
        # M.2 has less space for thermal routing
        self.bus_trace = RTTraceRoute(copper_oz=1.5, trace_width_mm=2.0, length_mm=40.0)

class Gyroscope_USB(_BaseGyroHardware):
    """
    External Diagnostic USB-HX Gyroscope.
    Used by ground technicians. Connects via an external, shielded analog cable.
    """
    def __init__(self):
        super().__init__()
        self.bus_trace = RTTraceRoute(copper_oz=1.0, trace_width_mm=1.0, length_mm=1000.0) # 1 meter cable

class Gyroscope_Serial(_BaseGyroHardware):
    """
    Univac-Compliant Serial Gyroscope.
    Extremely slow, sequential data output, but mathematically indestructible.
    Used for legacy SCADA integration.
    """
    def __init__(self):
        super().__init__()
        self.baud_rate = 9600
        
    def poll_serial_telemetry(self):
        raw_matrix = self.resonator.calculate_state_matrix()
        # Must send data one analog pulse at a time
        return [raw_matrix["GYRO_V"]]
