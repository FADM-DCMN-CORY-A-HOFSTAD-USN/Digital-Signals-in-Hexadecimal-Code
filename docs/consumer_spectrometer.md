To implement Ocean Insight (formerly Ocean Optics) as your immediate high-accuracy solution, the specific model you need for board-level integration is the Ocean ST Microspectrometer.

This is Ocean Insight's newest, most compact, and highest-performance "engine" designed specifically to be embedded onto a PCB while retaining full laboratory-grade accuracy.

The "Now" Solution: Ocean Insight Ocean ST
------------------------------------------

Unlike the older STS series, the Ocean ST provides higher sensitivity and broader spectral range in a footprint small enough (42 mm x 40 mm) to mount on your board.

-   Model to Order:  Ocean ST-VIS (Visible range, 350--810 nm) or Ocean ST-UV (185--650 nm) depending on your "full spectrum" needs.

-   Why it Fits:

-   Lab-Grade Resolution: It uses a physical cross-Czerny-Turner optical bench with a diffraction grating, offering optical resolution <1.5 nm (FWHM). This is significantly more accurate than standard chip-level sensors.

-   Direct Board Integration: It features a 16-pin Samtec header (Part: TFM-108-02-L-DH) on the side. You can design your PCB to mate directly with this header to supply power (5V) and communicate via RS-232 or USB 2.0 without bulky cables.

-   Thermal Stability: It is engineered with robust thermal management to prevent wavelength drift, which is critical if your board generates heat.

How to Integrate It (Pinout & Connectivity)
-------------------------------------------

You do not need to solder this device. You will design your board with a mating connector to plug the Ocean ST engine in like a cartridge.

-   Mating Connector: Your PCB should have a Samtec SFM-108-02-L-DH socket.

-   Key Pinout Signals:

-   Pin 1 & 2: Ground

-   Pin 3: VBUS (5V Power)

-   Pin 4 & 5: USB D- / D+ (For direct data to your PC/Processor)

-   Pin 11 & 12: UART TX/RX (For direct serial communication with a microcontroller)

-   Software SDK: Use OceanDirect SDK (available for C, C++, C#, Python, and MATLAB). This allows your "server" or local processor to pull raw spectral data, control integration times, and handle buffering automatically. [1]

Strategic Note: Ocean Insight vs. Torrent (PixelSensor)
-------------------------------------------------------

You mentioned using Torrent (Pixelteq/Salvo) for the "more expensive" version. Note that this is usually the reverse.

-   Ocean Insight (Spectrometer): Captures the continuous curve of light (thousands of data points). It is typically more expensive ($1,500--$2,500+ per unit) and higher accuracy. [2]

-   Torrent/PixelSensor (Multispectral Photodiode): Captures only 8 discrete bands. It is typically less expensive ($50--$200 per unit in volume) and lower resolution.

Recommendation: If your "server" version requires the absolute highest fidelity (e.g., detecting subtle chemical signatures or exact color shifts), stay with Ocean Insight. If the "server" version is for mass deployment where cost is key, switch to Torrent.
