Excellent. By hardwiring the 36-bit word structure directly into the I/O pinout of the Hex Chip, we eliminate the need for intermediate software translation. The chip will natively speak the language of the factory-floor PLC and the UNIVAC mainframe, achieving zero-latency telemetry.

Here is the foundational hardware specification to commit to the `Digital-Signals-in-Hexadecimal-Code` repository.

### File: `/hardware_specs/hex_chip_36bit_pinout.md`

**Component Designation:** Universal Hex-Telemetry Translation ASIC
**Target Architecture:** 36-Bit Parallel Output (UNIVAC-IX / PLC Compatible)
**Primary Application:** Square-Tooth Generator Phase Monitoring

#### I. Physical Pinout Architecture

To ensure seamless integration with legacy mainframe data buses, the chip utilizes a parallel data bus configuration alongside dedicated analog ingestion pins.

| Pin Group | Pin Identifiers | Function / Designation |
| --- | --- | --- |
| **Analog Ingestion** | `AIN_0` - `AIN_3` | Quad-phase inputs connecting directly to the concentric magnetic arrays. Reads raw square-tooth voltage. |
| **Mainframe Data Bus** | `D00` - `D35` | 36-pin parallel output bus. Streams the compiled hexadecimal word directly to the UNIVAC-IX system. |
| **PLC Handshake** | `CLK`, `RDY`, `ACK` | Clock synchronization, Data Ready (chip to mainframe), and Acknowledge (mainframe to chip). |
| **Hardware Bypass** | `ERR`, `ISO` | Flags localized hardware failures and isolates the fault without interrupting the main 36-bit stream. |

---

#### II. 36-Bit Word Hexadecimal Packaging

The internal logic of the Hex Chip will sample the `AIN` pins and compile the analog data into a single 36-bit word every clock cycle. The word is segmented as follows:

* **Bits 00-11 (Data Block A - Power):**
* *Function:* Real-time voltage amplitude and magnetic phase alignment.
* *Hex Range:* `0x000` to `0xFFF` (Mapping the exact crests and troughs of the square wave).


* **Bits 12-23 (Data Block B - Mechanics):**
* *Function:* Physical RPM, stator structural load, and thermal telemetry.
* *Hex Range:* `0x000` to `0xFFF`.


* **Bits 24-31 (Data Block C - Diagnostics):**
* *Function:* 8-bit hex sequence dedicated to error routing. If `ERR` pin goes high, this block broadcasts the exact sector of the concentric ring experiencing voltage drop.


* **Bits 32-35 (Data Block D - Control):**
* *Function:* 4-bit parity check and PLC routing flags to ensure the UNIVAC mainframe routes the data to the correct load-balancing queue.



---

#### III. Signal Conversion Logic

The analog-to-digital converter (ADC) inside the Hex Chip operates on a strict threshold logic tailored for square-tooth topologies. Because square waves do not have the gradual slopes of sinusoidal waves, the ADC logic is strictly binary at the micro-level:

1. **Rise Detect:** Voltage crosses `High` threshold $\rightarrow$ Hex Block A outputs `0xFFF`.
2. **Sustain:** Voltage maintains plateau $\rightarrow$ Hex Block A outputs `0xFFF`.
3. **Fall Detect:** Voltage crosses `Low` threshold $\rightarrow$ Hex Block A outputs `0x000`.

---

With the physical pinout and word structure defined in the Hex repository, should we draft the C/Assembly logic for the chip's internal ADC to handle this analog-to-hex conversion, or move over to the `Univac-IX` repository to write the PLC handshake protocol that will receive this data?
