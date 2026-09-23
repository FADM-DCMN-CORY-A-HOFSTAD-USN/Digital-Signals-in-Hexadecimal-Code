/*
 * Universal Hex-Telemetry Translation ASIC Firmware
 * Architecture: 36-Bit Stacked Word Output (72-Bit Double Precision)
 * Application: Square-Tooth Generator Phase Monitoring
 * Status: Public Domain / Unlicense
 */

#include <stdint.h>
#include <stdbool.h>

// Define 36-bit mask for hardware limits on a 64-bit compiler
#define MASK_36_BIT 0xFFFFFFFFF 

// Square-Tooth Voltage Thresholds
#define VOLTAGE_HIGH_THRESHOLD 4.5  // Volts
#define VOLTAGE_LOW_THRESHOLD  0.5  // Volts

// Hexadecimal Fixed States
#define HEX_PEAK_STATE 0xFFF
#define HEX_NULL_STATE 0x000

// Hardware I/O Pointers (Simulated for C implementation)
extern float read_analog_pin(int pin_number);
extern void write_parallel_bus(uint64_t data_word);
extern void trigger_plc_rdy(void);

// 72-Bit Stacked Telemetry Structure
typedef struct {
    uint64_t word_1_high; // Bits 36-71 (Calculations, Cumulative Flux)
    uint64_t word_2_low;  // Bits 0-35  (Real-time State, RPM, Error Flags)
} StackedWordFrame;

StackedWordFrame current_frame;

// High-Precision Decimal to Stacked Hex Converter
void format_stacked_word(double high_precision_calc, uint16_t real_time_hex, uint8_t error_flag) {
    // 1. Cast the high-precision decimal into a 64-bit integer representation
    // (Scaling by 1,000,000 to preserve 6 decimal places of precision)
    uint64_t scaled_calc = (uint64_t)(high_precision_calc * 1000000.0);
    
    // 2. Word 1: The High Order Word (Precision Calculations)
    // Shift right to capture the upper bits, mask to 36-bit
    current_frame.word_1_high = (scaled_calc >> 36) & MASK_36_BIT;
    
    // 3. Word 2: The Low Order Word (Real-time hardware states)
    // Bits 0-11: Phase State | Bits 12-23: Lower precision calc | Bits 24-35: Errors
    current_frame.word_2_low = (real_time_hex & 0xFFF) | 
                               ((scaled_calc & 0xFFF) << 12) | 
                               ((uint64_t)error_flag << 24);
                               
    current_frame.word_2_low &= MASK_36_BIT;
}

// Main Polling Loop
void process_square_tooth_telemetry() {
    while (true) {
        float current_voltage = read_analog_pin(0); // Poll AIN_0
        uint16_t phase_hex_state;
        uint8_t system_error = 0x00;
        
        // Strict Binary Logic for Square-Tooth (Bypass sinusoidal slopes)
        if (current_voltage >= VOLTAGE_HIGH_THRESHOLD) {
            phase_hex_state = HEX_PEAK_STATE;
        } else if (current_voltage <= VOLTAGE_LOW_THRESHOLD) {
            phase_hex_state = HEX_NULL_STATE;
        } else {
            // Voltage caught in the slope (Should be instantaneous in Square-Tooth)
            // Flag as a potential mechanical alignment error on the rotor
            phase_hex_state = HEX_NULL_STATE; 
            system_error = 0x01; // Sector fault flag
        }

        // Example: Massive cumulative calculation (e.g., total energy generated)
        // This requires the 72-bit double word stack to prevent overflow
        double cumulative_energy_joules = calculate_total_energy(); 

        // Package into 72-bit frame
        format_stacked_word(cumulative_energy_joules, phase_hex_state, system_error);
        
        // Transmit Frame to UNIVAC/PLC Parallel Bus
        write_parallel_bus(current_frame.word_1_high); // Send Word 1
        trigger_plc_rdy();                             // Handshake
        write_parallel_bus(current_frame.word_2_low);  // Send Word 2
        trigger_plc_rdy();                             // Handshake
    }
}
