import socket
import json
import numpy as np

def dispatch_task(node_ip, node_port, matrix_chunk):
    """Sends a workload slice to an external compute node."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((node_ip, node_port))
        
        payload = json.dumps({"matrix_chunk": matrix_chunk.tolist()})
        sock.sendall(payload.encode('utf-8'))
        sock.shutdown(socket.SHUT_WR)
        
        response_data = b""
        while True:
            packet = sock.recv(4096)
            if not packet:
                break
            response_data += packet
            
        sock.close()
        return json.loads(response_data.decode('utf-8'))
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}

def distribute_hex_simulation():
    # Example cluster setup: IPs of your other computers
    worker_nodes = [
        {"ip": "111.111.111.111", "port": 5001},  # Node 1
        {"ip": "112.112.112.112", "port": 5001}   # Node 2
    ]
    
    # Generate mock 1000x1000 silicon simulation grid (Voltages between 0.0V and 1.0V)
    print("[*] Generating 16-state simulation grid...")
    simulation_grid = np.random.choice(np.arange(0, 1.0625, 0.0625), size=(1000, 1000))
    
    # Divide work evenly among cluster computers
    chunks = np.array_split(simulation_grid, len(worker_nodes), axis=0)
    
    combined_results = []
    for idx, node in enumerate(worker_nodes):
        print(f"[*] Offloading partition {idx} to external machine {node['ip']}...")
        result = dispatch_task(node["ip"], node["port"], chunks[idx])
        
        if result.get("status") == "SUCCESS":
            print(f"[+] Finished processing partition {idx} successfully.")
            combined_results.extend(result["computed_data"])
        else:
            print(f"[-] Node {node['ip']} failed: {result.get('message')}")
            
    print(f"[+] Comprehensive network simulation complete. Aggregated matrix size: {len(combined_results)} rows.")

if __name__ == "__main__":
    distribute_hex_simulation()
