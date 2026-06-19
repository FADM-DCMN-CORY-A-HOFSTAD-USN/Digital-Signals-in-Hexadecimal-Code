class RTVaporChamberHeatsink:
    """
    Revolutionary Technology 3D Vapor Chamber Heatsink.
    The critical thermal bridge between the RT-PCM pad and the Centrifugal Blower.
    Utilizes internal capillary action to spread massive point-heat instantly.
    """
    def __init__(self, thermal_capacity_watts=350.0):
        self.thermal_capacity = thermal_capacity_watts
        
        # Internal physics state of the vapor chamber
        self.internal_fluid_state = "LIQUID"
        self.vaporization_point_c = 42.0 
        
        # The physical micro-fins that the blower fan cools
        self.fin_array_temp_c = 35.0

    def execute_capillary_cycle(self, point_heat_load_watts, chip_temp_c):
        """
        Processes the extreme heat dumped by the RT-PCM pad. 
        Spreads it laterally across the entire copper fin array in milliseconds.
        """
        print(f"\n[VAPOR CHAMBER] Absorbing {point_heat_load_watts:.1f}W point-load from RT-PCM pad...")
        
        # 1. Vaporization Phase (Boiling)
        if chip_temp_c >= self.vaporization_point_c and self.internal_fluid_state == "LIQUID":
            self.internal_fluid_state = "VAPOR"
            print("  -> [PHYSICS] Internal fluid vaporized. Heat spreading laterally at sonic speed.")
            
        # 2. Condensation and Heat Transfer
        if self.internal_fluid_state == "VAPOR":
            # The vapor hits the micro-fins, dumping the heat across the massive surface area
            self.fin_array_temp_c += (point_heat_load_watts * 0.15)
            print(f"  -> [PHYSICS] Heat saturated into micro-fins. Fin array temp: {self.fin_array_temp_c:.1f}°C.")
            
            # 3. Capillary Return
            self.internal_fluid_state = "LIQUID"
            print("  -> [PHYSICS] Fluid condensed. Copper wicks pulling coolant back to point-of-contact.")
            
        return self.fin_array_temp_c

    def apply_blower_cooling(self, cooling_reduction_c):
        """Allows the Centrifugal Blower to strip the heat out of the micro-fins."""
        self.fin_array_temp_c = max(30.0, self.fin_array_temp_c - cooling_reduction_c)
        return self.fin_array_temp_c
