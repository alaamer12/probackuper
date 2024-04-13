import psutil
import os
def get_partition_free_space(path='.', unit='GB'):
    """Get the free space of a partition and format it based on the specified unit."""
    unit_multiplier = {'GB': 1e9, 'MB': 1e6, 'Bytes': 1}

    try:
        usage = psutil.disk_usage(path).free
    except Exception as e:
        return f"Error: {e}"

    return f"{usage / unit_multiplier[unit]:.2f} {unit}"

# Example usage
print(get_partition_free_space('C:\\', 'GB'))  # Get free space of the C: drive in GB
print(get_partition_free_space('D:\\', 'GB'))  # Get free space of the D: drive in MB
print(get_partition_free_space('E:\\', 'Bytes'))  # Get free space of the E: drive in Bytes


def _list_root_dirs(self, partition: str) -> list:
    return [os.path.join(partition, d) for d in os.listdir(partition) if
            os.path.join(partition, d) not in self._exclude_dirs(os.path.join(partition, d))]