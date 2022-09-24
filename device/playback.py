from device import Device

dev = Device('play')

@dev.register_root
def root(input):
    print(input)

dev.run()
