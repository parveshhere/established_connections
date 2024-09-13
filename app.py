import subprocess
import psutil

def get_established_connections_with_pid():
    # Run the netstat command to get connections with PID
    result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)

    connections = []
    # Loop through the output, and filter only ESTABLISHED connections
    for line in result.stdout.splitlines():
        if 'ESTABLISHED' in line:
            columns = line.split()
            protocol = columns[0]
            local_address = columns[1]
            foreign_address = columns[2]
            pid = columns[-1]

            try:
                # Get the process name and status using psutil
                process = psutil.Process(int(pid))
                process_name = process.name()
                status = process.status()
            except psutil.NoSuchProcess:
                process_name = "Unknown"
                status = "N/A"

            connections.append({
                'protocol': protocol,
                'local_address': local_address,
                'foreign_address': foreign_address,
                'pid': pid,
                'process_name': process_name,
                'status': status
            })

    return connections

# Display the detailed established connections with PID and process information
connections = get_established_connections_with_pid()
for connection in connections:
    print(f"Protocol: {connection['protocol']}")
    print(f"Local Address: {connection['local_address']}")
    print(f"Foreign Address: {connection['foreign_address']}")
    print(f"PID: {connection['pid']}")
    print(f"Process Name: {connection['process_name']}")
    print(f"Process Status: {connection['status']}")
    print("-" * 50)
