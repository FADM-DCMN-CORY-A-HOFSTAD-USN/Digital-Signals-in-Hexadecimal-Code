from ..hex_rt_infrastructure import RTTraceRoute, RTGuardRing

class HexNativeUSBController:
    """
    Universal Serial Bus Controller for Hexadecimal Peripherals (USB-HX).
    """
    def __init__(self, ports=8):
        self.ports = ports
        self.connected_devices = {}
        self.rt_guard_ring = RTGuardRing()
        
        # External peripherals can draw massive power; enforcing 2oz copper traces
        self.power_delivery_trace = RTTraceRoute(copper_oz=2.0, trace_width_mm=2.0, length_mm=100.0)

    def plug_device(self, port_number, device_name, draw_amps):
        if 0 <= port_number < self.ports:
            self.connected_devices[port_number] = {"name": device_name, "amps": draw_amps}
            print(f"[USB-HX] Native peripheral '{device_name}' connected to Port {port_number}.")

    def poll_peripheral_telemetry(self, port_number, raw_voltage_stream):
        """Ingests external logic streams and scrubs them for motherboard safety."""
        if port_number in self.connected_devices:
            amps = self.connected_devices[port_number]["amps"]
            
            # 1. Verify the trace can handle the peripheral's power draw
            safe_stream, heat_w = self.power_delivery_trace.transmit_analog_signal(amps, raw_voltage_stream)
            
            if safe_stream:
                # 2. Scrub the incoming external signal of noise before it hits the PCIe bus
                clean_stream = self.rt_guard_ring.isolate_logic_stream(safe_stream)
                return clean_stream
        return []
