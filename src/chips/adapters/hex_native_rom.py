class HexNativeEEPROM:
    """
    Electrically Erasable Programmable Read-Only Memory.
    Natively traps analog voltage signatures permanently to store the BIOS/UEFI bootloader.
    """
    def __init__(self):
        # The exact 16-state hardware instructions required to boot the Revolutionary Architecture
        self.firmware_boot_sequence = [0.0, 0.5, 0.8125, 1.0, 0.25, 0.0625]
        self.is_write_protected = True

    def initialize_system_boot(self):
        """Fires the trapped analog charges into the native CPU to begin the POST sequence."""
        print("[NATIVE ROM] Power detected. Executing primary hexadecimal bootloader...")
        return self.firmware_boot_sequence

    def flash_firmware(self, new_hex_sequence, unlock_key):
        """Allows updating the BIOS if the hardware write-protect is safely bypassed."""
        if not self.is_write_protected and unlock_key == "RT_ADMIN":
            self.firmware_boot_sequence = new_hex_sequence
            print("[NATIVE ROM] Firmware successfully updated to new 16-state logic block.")
        else:
            print("[NATIVE ROM] SECURITY HALT: Cannot flash firmware. Chip is write-protected.")
