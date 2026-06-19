import time
from ..hex_rt_infrastructure import RTTraceRoute, RTGuardRing, RTPhaseChangeThermalInterface

class ErbiumDopedFiberCore:
    """
    The Optical Cathode.
    A silica fiber doped with Trivalent Erbium ions (Er3+). 
    When energized, these ions suspend in an excited quantum state, ready to release photons.
    """
    def __init__(self):
        self.excitation_level = 0.0  # Percentage of excited Er3+ ions
        self.max_gain_db = 30.0      # Maximum optical gain

    def stimulate_emission(self, weak_input_signal, pump_energy):
        """
        The core physics of the optical tube. The weak incoming signal triggers 
        the excited Erbium ions to release identical photons, multiplying the 
        signal massively without electrical noise.
        """
        if pump_energy > 0:
            self.excitation_level = min(100.0, pump_energy * 20.0)
            
        # Amplification multiplier based on the Erbium excitation state
        amplification_factor = 1.0 + (self.excitation_level * 0.05)
        
        amplified_signal = weak_input_signal * amplification_factor
        return amplified_signal


class WavelengthDivisionMultiplexer:
    """
    The Optical Grid.
    Mixes the 980nm pump laser (power) with the 1550nm weak signal (data) 
    into the exact same fiber core without the wavelengths colliding.
    """
    def __init__(self):
        self.is_aligned = True

    def mix_signals(self, signal_wave, power_wave):
        # In a real WDM, these are combined passively via physical dichroic filters
        return signal_wave, power_wave


class HexNativeEDFA:
    """
    Native Hexadecimal Erbium-Doped Fiber Amplifier (EDFA-HX).
    The ultimate "Optical Vacuum Tube" replacement for the RT Architecture.
    Amplifies massive analogue matrices at the speed of light.
    """
    def __init__(self):
        # Internal Optical Components
        self.erbium_core = ErbiumDopedFiberCore()
        self.wdm_grid = WavelengthDivisionMultiplexer()
        
        # Pump Laser Diode (980nm) - The "Heater/Power Supply" of the tube
        self.pump_laser_mw = 500.0 
        
        # RT Physical Infrastructure (Lasers generate intense point-heat)
        self.rt_thermal_pad = RTPhaseChangeThermalInterface()
        self.rt_guard_ring = RTGuardRing()
        self.thermal_state_c = 30.0

    def amplify_optical_matrix(self, optical_voltage_matrix):
        """
        Takes a degraded or weak analogue matrix and blasts it through the 
        Erbium fiber, instantly amplifying the 16-state logic back to full strength.
        """
        print(f"\n[EDFA OPTICAL TUBE] Ingesting weak optical matrix ({len(optical_voltage_matrix)} variables)...")
        print(f"  -> Igniting 980nm Pump Laser at {self.pump_laser_mw}mW.")
        
        # 1. Scrub the incoming electrical triggers before optical conversion
        clean_matrix = self.rt_guard_ring.isolate_logic_stream(optical_voltage_matrix)
        
        amplified_matrix = []
        for weak_v in clean_matrix:
            # 2. The WDM mixes the weak data signal with the raw pump laser energy
            mixed_signal, mixed_power = self.wdm_grid.mix_signals(weak_v, self.pump_laser_mw)
            
            # 3. Stimulated Emission in the Erbium Core (Analogue Amplification)
            amplified_v = self.erbium_core.stimulate_emission(mixed_signal, mixed_power)
            
            # 4. Snap the amplified waveform perfectly back onto the 1V RT hexadecimal scale
            # (Ensuring the signal never exceeds Hex F / 1.0V)
            snapped_v = round(min(1.0, amplified_v) / 0.0625) * 0.0625
            amplified_matrix.append(snapped_v)

        # 5. Handle the thermal load of the 980nm Pump Laser
        heat_generated = (self.pump_laser_mw / 1000.0) * 15.0  # W to thermal load
        self.thermal_state_c += heat_generated
        self.thermal_state_c = self.rt_thermal_pad.dissipate_heat(self.thermal_state_c, heat_generated)
        
        print(f"[EDFA OPTICAL TUBE] Stimulated emission complete. Signal restored to strict 16-state RT logic.")
        return amplified_matrix
