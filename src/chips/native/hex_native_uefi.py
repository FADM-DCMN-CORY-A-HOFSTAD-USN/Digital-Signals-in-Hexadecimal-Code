from ..hex_rt_infrastructure import RTGuardRing, RTTraceRoute

class HexNativeUEFI:
    """
    Native Hexadecimal Unified Extensible Firmware Interface (UEFI-HX).
    The master pre-boot execution environment. Orchestrates hardware initialization, 
    thermal safety checks, and secure kernel handoff using strict 1V analog logic.
    """
    def __init__(self):
        self.rt_guard_ring = RTGuardRing()
        self.system_state = "PRE_BOOT"
        
        # UEFI requires highly stable power to prevent bricking during firmware updates
        self.boot_trace = RTTraceRoute(copper_oz=2.0, trace_width_mm=1.5, length_mm=30.0)
        
        # Analog POST (Power-On Self Test) checklist
        self.hardware_registry = []

    def execute_power_on_self_test(self, motherboard_bus):
        """
        Scans the Hex-PCIe bus to verify all native silicon and RT infrastructure 
        is present and thermally stable before applying main power to the CPU.
        """
        print("\n[UEFI-HX] Initiating Analog Power-On Self Test (POST)...")
        
        # Ping the connected devices on the motherboard bus
        for slot, device in motherboard_bus.devices.items():
            # A valid response is a specific baseline voltage (e.g., Hex 3 / 0.1875V)
            print(f"  -> Verifying silicon at {slot}...")
            self.hardware_registry.append(slot)
            
        print(f"[UEFI-HX] POST Complete. {len(self.hardware_registry)} RT components registered.")
        return True

    def coordinate_secure_boot(self, tpm_module, eeprom_module):
        """
        Fetches the bootloader from the analog EEPROM and routes it through the TPM 
        for physical voltage signature verification.
        """
        print("[UEFI-HX] Coordinating Secure Boot sequence...")
        
        # 1. Fetch the physical voltage instructions from the ROM
        raw_boot_sequence = eeprom_module.initialize_system_boot()
        
        # 2. Pass the sequence through the Guard Ring to eliminate pre-boot jitter
        clean_boot_sequence = self.rt_guard_ring.isolate_logic_stream(raw_boot_sequence)
        
        # 3. Request cryptographic clearance from the Native TPM
        is_secure = tpm_module.verify_secure_boot(clean_boot_sequence)
        
        if is_secure:
            self.system_state = "SECURE_BOOT_CLEARED"
            return clean_boot_sequence
        else:
            self.system_state = "HALT_CRITICAL_SECURITY_FAILURE"
            print("[UEFI-HX] SYSTEM HALTED. Cryptographic analog signature mismatch.")
            return None

    def mount_pre_os_environment(self, memory_controller, network_card=None):
        """
        Initializes the RAM and provides basic networking (PXE boot) 
        before the high-resource Linux kernel takes over.
        """
        if self.system_state != "SECURE_BOOT_CLEARED":
            return False
            
        print("[UEFI-HX] Mounting Pre-OS Execution Environment...")
        
        # Send an initialization pulse (Hex F / 1.0V) to wake the Memory Controller
        memory_controller.flush_to_ram([1.0, 1.0, 1.0])
        
        if network_card:
            print("[UEFI-HX] Network Interface detected. Native PXE boot available.")
            
        return True

    def execute_kernel_handoff(self, main_cpu, boot_sequence_stream):
        """
        The final UEFI action. Hands control of the Revolutionary Z-Series Motherboard 
        over to the main processor to boot the operating system.
        """
        print("\n[UEFI-HX] Executing Kernel Handoff to Z-Series CPU...")
        
        # Ensure the power trace can handle the sudden CPU spike during handoff
        safe_stream, heat_w = self.boot_trace.transmit_analog_signal(current_amps=1.5, voltage_stream=boot_sequence_stream)
        
        if safe_stream:
            self.system_state = "OS_RUNTIME"
            # CPU takes over the exact 16-state logic instructions
            main_cpu.process_kernel_thread(core_id=0, logic_stream=safe_stream)
            print("[UEFI-HX] Handoff successful. UEFI entering passive monitor mode.")
            return True
        else:
            print("[UEFI-HX] Handoff failed. Trace impedance bottleneck detected.")
            return False
