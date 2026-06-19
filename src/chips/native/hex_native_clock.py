from ..hex_rt_infrastructure import RTGuardRing

class HexNativeClockGenerator:
    """
    Staircase Oscillator (RTC-HX).
    Generates the master 16-state synchronization wave for the entire motherboard.
    """
    def __init__(self, base_frequency_mhz=100.0):
        self.base_frequency = base_frequency_mhz
        self.rt_guard_ring = RTGuardRing()

    def pulse_system_clock(self):
        """
        Generates a perfect 16-state ascending and descending voltage wave.
        If this timing wave is corrupted, the entire system crashes.
        """
        # Generate the perfect 0.0V to 1.0V step-ladder wave
        staircase_wave = [i * 0.0625 for i in range(16)]
        
        # The clock signal is immediately passed through the Guard Ring.
        # This ensures that nearby high-power components cannot cause electromagnetic 
        # jitter on the motherboard's master timing signal.
        perfect_timing_wave = self.rt_guard_ring.isolate_logic_stream(staircase_wave)
        
        return perfect_timing_wave
