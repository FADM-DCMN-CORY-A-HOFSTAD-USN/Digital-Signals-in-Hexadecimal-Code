import socket
import json
import numpy as np

def compute_voltage_matrix(data_chunk):
    """
    Simulates analog voltage transitions over an assigned chunk of matrix rows.
    Validates state decay over 16-state logic levels.
    """
    matrix = np.array(data_chunk)
    # Target 0.0625V intervals
    intervals = np.round(matrix / 0.0625) * 0.0625
    
    # Calculate simulated signal attenuation
    attenuation_factor = 0.998
    processed_matrix = np.clip(intervals * attenuation_factor, 0.0, 1.0)
    
    return processed_matrix.tolist()

def start_worker_node(host='0.0.0.0', port=5001):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"[*] Secondary compute node active. Listening on port {port}...")
    
    while True:
        client_socket, addr = server_socket.accept()
        print(f"[+] Connected to master engine at {addr}")
        
        data_buffer = b""
        while True:
            packet = client_socket.recv(4096)
            if not packet:
                break
            data_buffer += packet
            
        if data_buffer:
            try:
                payload = json.loads(data_buffer.decode('utf-8'))
                print(f"[*] Processing {len(payload['matrix_chunk'])} rows of HEX silicon data...")
                
                # Compute task via local CPU/GPU resource
                result = compute_voltage_matrix(payload['matrix_chunk'])
                
                # Return calculations
                response = json.dumps({"status": "SUCCESS", "computed_data": result})
                client_socket.sendall(response.encode('utf-8'))
            except Exception as e:
                error_resp = json.dumps({"status": "ERROR", "message": str(e)})
                client_socket.sendall(error_resp.encode('utf-8'))
                
        client_socket.close()

if __name__ == "__main__":
    # Run this on your secondary network hardware machines
    start_worker_node()
