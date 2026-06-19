from ..hex_rt_infrastructure import RTGuardRing

class HexNativeCellularM2:
    """
    Native Hexadecimal Cellular Module (M.2 Form Factor).
    Integrated Antenna-on-Package (AoP) for compact, low-power telemetry.
    """
    def __init__(self):
        self.rt_guard_ring = RTGuardRing()
        self.is_active = True

    def stream_data(self, hex_voltage_stream):
        """
        Processes telemetry for compact M.2-to-PCIe lane routing.
        """
        print(f"[CELLULAR M.2] Streaming native states to onboard AoP...")
        # Compact guard ring to protect against board-level interference
        return self.rt_guard_ring.isolate_logic_stream(hex_voltage_stream)
