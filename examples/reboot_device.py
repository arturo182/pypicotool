from picotool import reboot


# you can reboot a device:
reboot()

# or if you have more than one, you can specify the device to reboot:
reboot(bus=1, address=10)
