### The Ultimate RT Thermal Triad

With this heatsink integrated, your high-draw components (like the Unlocked Z-Series CPU or the Quad-M.2 Expander) now execute a perfect, three-stage physical cooling loop.

Here is how the logic flows when a massive computational load hits the system:

1.  **The Grab (Phase-Change):** The `RTPhaseChangeThermalInterface` liquefies, eliminating microscopic air gaps and grabbing the massive heat spike directly from the bare silicon die.

2.  **The Spread (Vapor Chamber):** The heat transfers into the `RTVaporChamberHeatsink`. The internal liquid instantly vaporizes, spreading the heat perfectly across hundreds of copper micro-fins.

3.  **The Exhaust (Centrifugal Blower):** Once the micro-fins heat up, the `RTCentrifugalBlower` drops its 0dB silent mode, spools up past 3,000 RPM, and blasts the hot air (and any dust particles) entirely out the back of the chassis.

You can easily upgrade your `HexNativeCPU` or `HexM2PCIeExpander` `__init__` functions to include `self.rt_vapor_chamber = RTVaporChamberHeatsink()`, placing it mathematically between your existing thermal pad and blower objects.
