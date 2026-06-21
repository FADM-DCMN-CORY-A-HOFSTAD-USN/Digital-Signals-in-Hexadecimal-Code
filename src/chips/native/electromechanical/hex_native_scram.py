from ..hex_rt_infrastructure import RTGuardRing, RTTraceRoute

class HexNativeEmergencySCRAM:
    """
    Hardware-Level SCRAM Circuit for the Antigravity Drive and Reactor.
    Physically drops the master voltage line and dumps reactor power to the 
    Guard Rings before the main CPU even registers the event.
    """
    def __init__(self):
        self.rt_guard_ring = RTGuardRing()
        
        # A massive 3oz copper trace designed exclusively to survive a one-time, 
        # catastrophic current dump from the main reactor to the ground plane.
        self.reactor_dump_trace = RTTraceRoute(copper_oz=3.0, trace_width_mm=5.0, length_mm=20.0)
        self.is_scrammed = False

    def monitor_critical_systems(self, hull_integrity_v, reactor_core_v):
        """
        Listens to the raw, uninterrupted analog line from the hull and reactor.
        """
        if self.is_scrammed:
            return "[SCRAM-HX] SYSTEM LOCKED. MANUAL HARDWARE RESET REQUIRED."
            
        # Hull breach (voltage drops to 0) OR Reactor surge (voltage exceeds 1.0V)
        if hull_integrity_v <= 0.0 or reactor_core_v > 1.0:
            return self._trigger_hardware_interrupt(reactor_core_v)
            
        return "[SCRAM-HX] Systems nominal. Monitoring..."

    def _trigger_hardware_interrupt(self, surge_voltage):
        """Violently grounds the system to prevent ship destruction."""
        print("\n[SCRAM-HX] !!! CRITICAL FAILURE DETECTED !!!")
        print("[SCRAM-HX] FIRING PHYSICAL HARDWARE INTERRUPT. BYPASSING CPU.")
        
        self.is_scrammed = True
        
        # Dump the massive electrical surge directly into the Guard Ring
        grounded_stream = self.rt_guard_ring.isolate_logic_stream([surge_voltage])
        
        # Push the remaining current through the 3oz dump trace
        safe_stream, _ = self.reactor_dump_trace.transmit_analog_signal(current_amps=15.0, voltage_stream=[1.0])
        
        print("[SCRAM-HX] Airlocks mechanically sealed. Reactor offline. Power dumped to ground.")
        return "[SCRAM-HX] SCRAM COMPLETE. SHIP SECURED."
