import psutil
import typer

def get_mountpoints():

    for partition in psutil.disk_partitions():
        print(partition.mountpoint)
        print(partition.fstype)

get_mountpoints()