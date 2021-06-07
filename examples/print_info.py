from picotool import info
import json

# pretty print the info, can be zero, one, or more devices
print(json.dumps(info(), indent=4))

# if you have more than one board, you can specify the bus and address:
print(info(bus=1, address=10))

# you can also get info on a file:
print(info(filename='/home/your/path/here.uf2'))
