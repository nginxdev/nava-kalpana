import psutil
import platform
from datetime import datetime


def get_size(bytes, suffix="B"):
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


# System Information
print("=" * 20, "System Information", "=" * 20)
uname = platform.uname()
print(f"OperatingSystem: {uname.system} {uname.release} ({uname.version})")
print(f"MachineName: {uname.node}")
print(f"CPU: {uname.machine},{uname.processor}")

boot_time_timestamp = psutil.boot_time()
boot_time = datetime.fromtimestamp(boot_time_timestamp)
print(f"BootTime: {boot_time.year}/{boot_time.month}/{boot_time.day}"
      f" {boot_time.hour}:{boot_time.minute}:{boot_time.second}")

print("=" * 20, "CPU Info", "=" * 20)
print("PhysicalCores:", psutil.cpu_count(logical=False))
print("TotalCores:", psutil.cpu_count(logical=True))
print(f"MaxFrequency: {psutil.cpu_freq().max:.2f}Mhz")
print(f"MinFrequency: {psutil.cpu_freq().min:.2f}Mhz")
print(f"CurrentFrequency: {psutil.cpu_freq().current:.2f}Mhz")

print("CPU Usage Per Core:")
for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
    print(f"Core {i}: {percentage}%")
print(f"Total CPU Usage: {psutil.cpu_percent()}%")

# RAM Information
print("=" * 20, "RAM Information", "=" * 20)
ram = psutil.virtual_memory()
print(f"Total: {get_size(ram.total)}")
print(f"Used: {get_size(ram.used)}")
print(f"Available: {get_size(ram.available)}")
print(f"Percentage: {ram.percent}%")
print("=" * 20, "SWAP", "=" * 20)
# get the swap memory details (if exists)
swap = psutil.swap_memory()
print(f"Total: {get_size(swap.total)}")
print(f"Free: {get_size(swap.free)}")
print(f"Used: {get_size(swap.used)}")
print(f"Percentage: {swap.percent}%")

# Disk Information
print("=" * 40, "Disk Information", "=" * 40)
print("Partitions and Usage:")
# get all disk partitions
partitions = psutil.disk_partitions()
for partition in partitions:
    print(f"=== Device: {partition.device} ===")
    print(f"  Mountpoint: {partition.mountpoint}")
    print(f"  File system type: {partition.fstype}")
    try:
        partition_usage = psutil.disk_usage(partition.mountpoint)
    except PermissionError:
        # this can be catched due to the disk that
        # isn't ready
        continue
    print(f"  Total Size: {get_size(partition_usage.total)}")
    print(f"  Used: {get_size(partition_usage.used)}")
    print(f"  Free: {get_size(partition_usage.free)}")
    print(f"  Percentage: {partition_usage.percent}%")
# get IO statistics since boot
disk_io = psutil.disk_io_counters()
print(f"Total read: {get_size(disk_io.read_bytes)}")
print(f"Total write: {get_size(disk_io.write_bytes)}")

'''
# Network information
print("=" * 40, "Network Information", "=" * 40)
# get all network interfaces (virtual and physical)
if_addrs = psutil.net_if_addrs()
for interface_name, interface_addresses in if_addrs.items():
    for address in interface_addresses:
        print(f"=== Interface: {interface_name} ===")
        if str(address.family) == 'AddressFamily.AF_INET':
            print(f"  IP Address: {address.address}")
            print(f"  Netmask: {address.netmask}")
            print(f"  Broadcast IP: {address.broadcast}")
        elif str(address.family) == 'AddressFamily.AF_PACKET':
            print(f"  MAC Address: {address.address}")
            print(f"  Netmask: {address.netmask}")
            print(f"  Broadcast MAC: {address.broadcast}")
# get IO statistics since boot
net_io = psutil.net_io_counters()
print(f"Total Bytes Sent: {get_size(net_io.bytes_sent)}")
print(f"Total Bytes Received: {get_size(net_io.bytes_recv)}")
'''

# GPU information
import GPUtil
from tabulate import tabulate

print("=" * 40, "GPU Details", "=" * 40)
gpus = GPUtil.getGPUs()
list_gpus = []
print(len(gpus))
for gpu in gpus:
    # get the GPU id
    gpu_id = gpu.id
    # name of GPUGP
    gpu_name = gpu.name
    # get % percentage of GPU usage of that GPU
    gpu_load = f"{gpu.load * 100}%"
    # get free memory in MB format
    gpu_free_memory = f"{gpu.memoryFree}MB"
    # get used memory
    gpu_used_memory = f"{gpu.memoryUsed}MB"
    # get total memory
    gpu_total_memory = f"{gpu.memoryTotal}MB"
    # get GPU temperature in Celsius
    gpu_temperature = f"{gpu.temperature} °C"
    gpu_uuid = gpu.uuid
    list_gpus.append((
        gpu_id, gpu_name, gpu_load, gpu_free_memory, gpu_used_memory,
        gpu_total_memory, gpu_temperature, gpu_uuid
    ))

print(tabulate(list_gpus, headers=("id", "name", "load", "free memory", "used memory", "total memory",
                                   "temperature", "uuid")))
