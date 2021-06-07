from picotool import load, verify


# you can just load a file:
print(load('/home/your/path/here.uf2'))

# or you can load and verify:
print(load('/home/your/path/here.elf', verify=True))

# you can also have a progress callback:
def progress_callback(progress, is_verify):
    print('%s Progress: %d%%' % ('Verify' if is_verify else 'Load', progress))

print(load('/home/your/path/here.uf2', verify=True, callback=progress_callback))

# or you can just verify:
print(verify('/home/your/path/here.uf2'))

# there's even more options:
print(load('/home/your/path/here.bin', verify=True, execute=True, bus=1, address=10, offset='0x10000000', mem_range=(0, 100))
