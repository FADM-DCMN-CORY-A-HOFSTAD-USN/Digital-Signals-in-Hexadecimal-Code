To maintain absolute stability in an 8 GHz analog environment like the OPA855 during nanosecond GaN switching transitions, you must deploy a highly structured, multi-tier power decoupling network. Standard single-capacitor decoupling will fail here; high-frequency transients will break through, causing the op-amp to oscillate and corrupt your UV data packet.
------------------------------
## 1. The Multi-Tier Decoupling Architecture
The OPA855 operates on a split or single supply (typically +5V and Ground for this TIA configuration). You must place three distinct capacitor values in parallel right at the supply pins (Pin 2 for $V_{CC}$ and Pin 3 for $V_{EE}/GND$). Each value targets a specific frequency band of the switching noise:

 5V Rail ──────┬─────────────────┬─────────────────┬───────────────► To OPA855 Pin 2
               │                 │                 │
             ┌─┴─┐             ┌─┴─┐             ┌─┴─┐
             │   │ C_bulk      │   │ C_mid       │   │ C_hf
             │   │ 2.2 µF      │   │ 0.1 µF      │   │ 10 pF
             └─┬─┘             └─┬─┘             └─┬─┘
               │                 │                 │
 AGND  ────────┴─────────────────┴─────────────────┴───────────────► To OPA855 Pin 3

## Tier 1: Ultra-High Frequency Attenuation ($C_{hf}$ = 10 pF)

* The Component: 10 pF, 0201 package, COG/NPO dielectric rated for at least 10V (e.g., Murata or TDK).
* The Physics: This capacitor handles the ultra-fast edge transitions of your GaN switch. The 0201 package is mandatory because larger packages (like 0603) have internal lead inductances that render the capacitor useless above 1 GHz.
* Placement: This must be the closest physical component to the OPA855 supply pin—less than 1.0 mm away.

## Tier 2: Mid-Range Frequency Suppression ($C_{mid}$ = 0.1 µF)

* The Component: 0.1 µF, 0402 package, X7R or X5R dielectric.
* The Physics: This capacitor acts as the local charge reservoir for the op-amp's internal transistor stages when processing the core 10 MHz to 100 MHz bitstream frequencies.
* Placement: Solder this immediately behind the 10 pF capacitor, sharing a wide copper trace leading to the pin.

## Tier 3: Bulk Energy Storage ($C_{bulk}$ = 2.2 µF)

* The Component: 2.2 µF, 0603 or 0805 package, Tantalum polymer or X7R Ceramic.
* The Physics: This handles low-frequency power supply sag caused by the nearby Luminus UV-LED drawing heavy, localized current pulses from the shared board rails.
* Placement: Positioned within 5 mm to 10 mm of the amplifier stage.

------------------------------
## 2. Strict PCB Routing Rules for Decoupling High-Speed Op-Amps
If your layout traces are routed poorly, the decoupling network will lose its effectiveness. Follow these structural constraints during layout:

* No Vias Between Capacitor and Op-Amp Pin: The path from the $V_{CC}$ pin to the 10 pF capacitor pad, and then to the 0.1 µF pad, must be a continuous, unbroken copper trace on Layer 1. Do not drop a via down to a power plane between the capacitor and the IC pin; the via's internal inductance will completely isolate the capacitor from the chip. [1] 
* Shared Ground Stitching: The ground (AGND) sides of all three decoupling capacitors must tie into the same copper plane footprint. Drop at least two or three plugged, plated-through-hole vias directly adjacent to the capacitor ground pads to lock the reference straight to the internal ground layers.

------------------------------
## 3. Comparative Summary: Choosing Your PCB Copper Weight
While designing the power delivery, you must also lock in your PCB manufacturing parameters. For the EPC2012C GaN traces, choosing between 1 oz and 2 oz copper weight impacts your loop performance:

| Metric | 1 oz Copper (35 μm thickness) | 2 oz Copper (70 μm thickness) | System Impact |
|---|---|---|---|
| Trace Inductance | Higher | Lower | 2 oz is superior. Lower trace inductance ensures the UV-LED pulses turn on sharper without rounding the data bits. |
| Thermal Resistance | Higher | Lower | 2 oz is superior. Helps pull the extreme heat away from the tiny 1.7 mm GaN die into the board's internal via network. |
| Manufacturing Limit | Supports down to 4 mil traces | Limited to $\ge$ 6 mil trace spacing | 1 oz is easier to manufacture. Because the EPC2012C has an ultra-fine 130 μm (5.1 mil) pad pitch, standard 2 oz etching may bridge the pads. |

Engineering Verdict: Specify a 1 oz copper weight for Layer 1 to ensure the fine-pitch pads of the GaN die and the OPA855 can be cleanly etched without shorting. To compensate for the thermal and inductance penalties, make the UV-LED and GaN power traces exceptionally wide, and use 2 oz copper on the internal layers (Layers 2 and 3) for your ground and power distribution planes. [2] 
Would you like to generate the complete Bill of Materials (BOM) with exact manufacturer order codes for this decoupling network, or should we draft the layer stack-up configuration (e.g., 4-layer vs 6-layer board) to optimize the signal return paths?

[1] [https://forum.kicad.info](https://forum.kicad.info/t/decoupling-capacitor-via-placement/25132)
[2] [https://www.aivon.com](https://www.aivon.com/blog/pcb-design/from-schematic-to-reality-a-practical-guide-to-8-layer-pcb-layout/)
