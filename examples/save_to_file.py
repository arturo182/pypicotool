from picotool import save


# you can just save only the installed program to file:
print(save('/home/your/path/here.uf2'))

# or you can save the whole flash:
print(save('/home/your/path/here.elf', all_flash=True))

# you can also have a progress callback:
def progress_callback(progress):
    print('%s Progress: %d%%' % ('Save', progress))

print(save('/home/your/path/here.uf2', all_flash=True, callback=progress_callback))

# there's even more options:
print(load('/home/your/path/here.bin', all_flash=True, bus=1, address=10, mem_range=(0, 100))
