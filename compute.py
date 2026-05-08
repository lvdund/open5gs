"""
Lightweight Resource Monitor using /proc filesystem
Timestamp format: HH:MM:SS
"""

import csv
import signal
import sys
import time
from datetime import datetime

running = True

def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully"""
    global running
    print("\n\nShutting down monitor...")
    running = False

def get_cpu_usage():
    """Get CPU usage from /proc/stat"""
    with open('/proc/stat', 'r') as f:
        cpu_line = f.readline().strip().split()
    
    # Calculate CPU usage from two readings
    cpu_times = [int(x) for x in cpu_line[1:]]
    idle_time = cpu_times[3]
    total_time = sum(cpu_times)
    
    return idle_time, total_time

def get_ram_usage():
    """Get RAM usage from /proc/meminfo"""
    mem_info = {}
    with open('/proc/meminfo', 'r') as f:
        for line in f:
            if 'MemTotal' in line or 'MemAvailable' in line:
                parts = line.split()
                mem_info[parts[0].rstrip(':')] = int(parts[1])
    
    used_memory = mem_info['MemTotal'] - mem_info['MemAvailable']
    ram_percent = (used_memory / mem_info['MemTotal']) * 100
    
    return ram_percent

def main():
    # Register signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"resource_usage_{timestamp}.csv"
    
    print(f"Starting resource monitor...")
    print(f"Logging to: {filename}")
    print(f"Press Ctrl+C to stop\n")
    
    try:
        with open(filename, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(['Timestamp', 'CPU_%', 'RAM_%'])
            csvfile.flush()
            
            # Print header for console output
            print(f"{'Timestamp':<10} {'CPU %':<10} {'RAM %':<10}")
            print("-" * 30)
            
            # Get initial CPU values
            prev_idle, prev_total = get_cpu_usage()
            
            while running:
                try:
                    time.sleep(1)
                    
                    # Get current timestamp in HH:MM:SS format
                    current_time = datetime.now().strftime("%H:%M:%S")
                    
                    # Calculate CPU usage
                    current_idle, current_total = get_cpu_usage()
                    idle_diff = current_idle - prev_idle
                    total_diff = current_total - prev_total
                    
                    if total_diff > 0:
                        cpu_percent = (1 - idle_diff / total_diff) * 100
                    else:
                        cpu_percent = 0.0
                    
                    prev_idle, prev_total = current_idle, current_total
                    
                    # Get RAM usage
                    ram_percent = get_ram_usage()
                    
                    # Write to CSV file
                    csv_writer.writerow([current_time, f"{cpu_percent:.1f}", f"{ram_percent:.1f}"])
                    csvfile.flush()
                    
                    # Print to console
                    print(f"{current_time:<10} {cpu_percent:<10.1f} {ram_percent:<10.1f}")
                    
                except Exception as e:
                    print(f"Error collecting data: {e}", file=sys.stderr)
                    csv_writer.writerow([datetime.now().strftime("%H:%M:%S"), "ERROR", "ERROR"])
                    csvfile.flush()
    
    except PermissionError:
        print(f"Error: Permission denied to write to {filename}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)
    
    print(f"\nMonitoring stopped. Data saved to: {filename}")
    print(f"Total entries logged: {sum(1 for _ in open(filename)) - 1}")  # -1 for header

if __name__ == "__main__":
    main()
