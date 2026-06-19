import os
import importlib.util
import concurrent.futures
import multiprocessing

def load_virtual_silicon(chips_dir='chips'):
    """
    Dynamically scans the chips directory and loads all hardware modules.
    This acts like a motherboard BIOS detecting installed hardware on boot.
    """
    loaded_classes = {}
    current_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.join(current_dir, chips_dir)

    print(f"[BIOS] Scanning PCIe slots in {target_dir}...")
    
    if not os.path.exists(target_dir):
        print(f"[BIOS] ERROR: Directory {target_dir} not found.")
        return loaded_classes

for root, _, files in os.walk(target_dir):
        for filename in files:
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = filename[:-3]
                filepath = os.path.join(root, filename)
            
            # Dynamically load the module
            spec = importlib.util.spec_from_file_location(module_name, filepath)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            # Extract classes from the loaded module
            for attr_name in dir(module):
                attr = getattr(module, attr_name)
                if isinstance(attr, type):  # If it's a class
                    folder_path = os.path.relpath(root, target_dir)
                        print(f"  -> Detected Silicon: {attr_name} (Location: {folder_path})")

    return loaded_classes

def execute_core_instruction(voltage_op):
    """
    Simulates a single core processing a hexadecimal voltage state.
    This function must be at the top level for Python multiprocessing to pickle it.
    """
    # e.g., 0.875V (Hex D)
    if voltage_op == 0.875:
        return f"[Core {multiprocessing.current_process().name}] Hardware Interrupt Processed at {voltage_op}V"
    else:
        return f"[Core {multiprocessing.current_process().name}] Executed Hex Logic at {voltage_op}V"

if __name__ == "__main__":
    print("="*50)
    print("INITIALIZING HEXADECIMAL ARCHITECTURE")
    print("="*50)

    # 1. Dynamically load all chip modules from src/chips/
    hardware = load_virtual_silicon()

    # Verify core components were found before proceeding
    required_chips = ['HexPCIeBus', 'HexCPU', 'HexAcceleratorCard']
    missing_chips = [chip for chip in required_chips if chip not in hardware]
    
    if missing_chips:
        print(f"[BIOS HALT] Missing critical silicon: {missing_chips}")
        exit()

    # 2. Build the RT Physical Motherboard and Native PCIe Bus
    rt_physical_board = hardware['RevolutionaryZSeriesMotherboard']()
    motherboard_bus = hardware['HexNativePCIe'](lanes=128) 

    # 3. Initialize Multicore CPU
    physical_cores = multiprocessing.cpu_count()
    main_cpu = hardware['HexNativeCPU'](cores=physical_cores)
    #motherboard_bus.plug_device("CPU_0", main_cpu)
    motherboard_bus = hardware['HexPCIeBus'](lanes=64)
    print(f"[SYSTEM] Initialized HexCPU with {physical_cores} active parallel cores.")
    
    # 5. Initialize NVIDIA Tensor Accelerator
    # Configured for high-throughput 16-state logic matrix math
    nvidia_gpu = hardware['HexAcceleratorCard'](type="NVIDIA_RTX_TENSOR_HEX")
    motherboard_bus.plug_device("GPU_NVIDIA_0", nvidia_gpu)

    # 6. Multicore Processing Simulation (The parallel execution payload)
    print("\n" + "="*50)
    print("COMMENCING MULTICORE HEX-VOLTAGE EXECUTION")
    print("="*50)

    # A burst of hexadecimal analog signals (e.g., telemetry or heavy matrix data)
    # Hex values represented as voltages: 7, C, F, 3, D, A, 0, 8
    incoming_telemetry_stream = [0.5, 0.8125, 1.0, 0.25, 0.875, 0.6875, 0.0, 0.5625]

    # Use ProcessPoolExecutor to distribute the voltage array across physical CPU cores
    with concurrent.futures.ProcessPoolExecutor(max_workers=physical_cores) as executor:
        # Map the voltage instructions to the parallel cores
        results = executor.map(execute_core_instruction, incoming_telemetry_stream)
        
        for output in results:
            print(output)

    # 6. Offload matrix math to the NVIDIA Tensor Core
    print("\n[SYSTEM] Offloading remaining telemetry matrix to NVIDIA Accelerator...")
    processed_matrix = nvidia_gpu.receive_data(incoming_telemetry_stream)
    print(f"[NVIDIA_RTX_TENSOR_HEX] Output Matrix Voltages: {processed_matrix}")
    print(f"[NVIDIA_RTX_TENSOR_HEX] Thermal State: {nvidia_gpu.thermal_state_c:.1f}°C")
