The best American-made scientific timing instrument to measure the propagation delay between your sensor and LED is the Stanford Research Systems (SRS) DG645 Digital Delay Generator.

Based in Sunnyvale, California, SRS is the global scientific standard for sub-nanosecond precision timing and metrology [1].

* * * * *

The Core Instrumentation Solution
----------------------------------------------

Stanford Research Systems (SRS) DG645
-------------------------------------

The DG645 is a high-accuracy, benchtop digital delay generator that can be easily integrated into automated test racks or server environments.

-   Accuracy & Resolution: Offers 5-picosecond delay resolution with an ultra-low jitter of <25 picoseconds relative to your trigger source [1].

-   Interface & Control: Features standard GPIB, Ethernet, and RS-232 interfaces, allowing your server or local software to programmatically arm, trigger, and pull timing data [1].

-   Price & Class: This is a premium, laboratory-grade instrument (typically $4,000--$6,000+) designed for high-end optical physics, semiconductor testing, and precision spectroscopy.

-   Documentation: You can view the formal timing specs and integration instructions directly on the [Stanford Research Systems DG645 Product Page](https://www.thinksrs.com/products/dg645.html).

The High-Performance Alternative: Chroma Systems Solutions
----------------------------------------------------------

If you need an instrument configured specifically for automated production lines or high-throughput component testing, Chroma Systems Solutions (headquartered in Foothill Ranch, California) manufactures the Chroma 52900 Series Programmable Time/Frequency Counters. This system slots directly into PXI/PXIe chassis slots on your testing board setups to measure the exact delta ($\Delta t$) between two electrical logic thresholds.

* * * * *

1\. The Circuit Constraint: Resolving the "Series" Issue
---------------------------------------------------------------------

Before connecting an advanced scientific timer to your setup, there is a fundamental electrical bottleneck that must be corrected: You cannot measure a time delay if the sensor and the LED are wired strictly in series.

In a pure series circuit, current must flow through both components simultaneously. The moment the sensor switches "on" and allows current to pass, that exact same current loop instantly energizes the LED. Electrically, there is zero time delay ($\Delta t = 0$) along a single continuous trace.

The Scientific Fix (Parallel Sense Points)
------------------------------------------

To capture the true physical propagation delay (the time it takes the silicon inside the sensor to react, switch, and drive the LED), you must isolate their signals into distinct Start and Stop logic channels:

               +5V / VCC\
                  │\
          ┌───────┴───────┐\
          │               │\
    ┌────┴────┐     ┌────┴────┐\
    │  Sensor │     │   LED   │\
    └────┬────┘     └────┬────┘\
          │               │\
          ├───► START     ├───► STOP\
          │   (Channel A) │   (Channel B)\
          ▼               ▼\
        To MCU/Driver   To Ground

1.  Channel A (START): Tap the output pin of your sensor. The moment it triggers high (or low), it sends a pulse to the Start/Trigger input of the SRS DG645.

2.  Channel B (STOP): Tap the anode or cathode of your LED. The moment the current driver pulls the line to illuminate the LED, that voltage change sends a pulse to the Stop/Inhibit input of the timer.

* * * * *

2\. Implementing the Test Configuration
----------------------------------------------------

To execute this measurement with scientific accuracy, structure your test sequence as follows:

1.  Set Threshold Voltages: Configure the input channels on your SRS timing instrument to match your circuit's logic level (e.g., $+3.3\text{ V}$ or $+5\text{ V}$ TTL thresholds).

2.  Minimize Parasitic Capacitance: Keep your oscilloscope or timer probe traces as short as possible. Long wires act as capacitors, artificially slowing down the rise time of your signals and introducing measurement errors.

3.  Account for Cable Propagation Delay: Standard coaxial cables (like RG-58) delay an electrical signal by roughly 1.5 to 2 nanoseconds per foot. Ensure the BNC cables running from your sensor board to the timer are the exact same length, or calibrate out the cable differential in the instrument software.

✅ Final Answer Summary
----------------------

The most accurate American scientific instrument to measure this time differential is the Stanford Research Systems DG645 Digital Delay Generator [1]. By tapping separate Start and Stop voltage nodes on your circuit layout, you can measure the true propagation delay down to 5-picosecond resolution [1].

What is the estimated time scale of the delay you are trying to capture (e.g., milliseconds, microseconds, or nanoseconds)? If you know the operating voltage of your board circuit, I can recommend the exact probe interfaces you'll need.
