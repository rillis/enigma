import string, sys, os

def add(x, y):
    return (x + y) % 26

def subtract(x, y):
    return (x - y + 26) % 26  # Adiciona 26 para evitar valores negativos

def char_num(letter):
    return ord(letter) - ord('a')

def num_char(num):
    return chr(num + ord('a'))

def configure_plugboard(pc):
    pb = {}
    for x in pc:
        pb[x] = pc[x]
        pb[pc[x]] = x
    for x in string.ascii_lowercase:
        if x not in pb:
            pb[x] = x
    return pb

def invert_mapping(mapping):
    return {v: k for k, v in mapping.items()}

def rotate_disk(disk):
    new_disk = [disk[0], disk[1], disk[2]]
    new_disk[0] += 1
    if new_disk[0] > 25:
        new_disk[0] = 0
        new_disk[1] += 1
    if new_disk[1] > 25:
        new_disk[1] = 0
        new_disk[2] += 1
    if new_disk[2] > 25:
        new_disk[2] = 0
    return new_disk

def inverse_disks(disks):
    return [{v: k for k, v in disk.items()} for disk in disks]


# ------------ start "constants"
# random generated disks
for x in ['disk0.enigma', 'disk1.enigma', 'disk2.enigma', 'disk3.enigma', 'disk4.enigma', 'diskI.enigma', 'diskF.enigma']:
    if not os.path.isfile("disks/"+x):
        print("Disks not generated/loaded, please run random_disks.py")
        sys.exit()

disks = []
for disk_n in range(5):
    with open(f'disks/disk{disk_n}.enigma', 'r') as f:
        disks.append(eval(f.read()))

with open(f'disks/diskI.enigma', 'r') as f:
    connector_start = eval(f.read())
with open(f'disks/diskF.enigma', 'r') as f:
    connector_end = eval(f.read())

# ------------ config
disk_order = None
plugboard_config = None
disk_rotation = None
with open('config.cfg', 'r') as file:
    lines = file.readlines()
for line in lines:
    exec(line)

# ------------ run
plugboard = configure_plugboard(plugboard_config)

complete_input = input("-> ").lower()
result = ""

for letter in complete_input:
    if letter in string.ascii_lowercase:
        actual = char_num(letter)

        # Through plugboard
        actual = char_num(plugboard[num_char(actual)])


        # Forward through connectors and rotors
        actual = connector_start[actual]

        for i in range(3):
            temp = add(actual, disk_rotation[i])
            actual = disks[disk_order[i]][temp]
            actual = subtract(actual, disk_rotation[i])

        actual = connector_end[actual]

        for i in range(2, -1, -1):
            temp = add(actual, disk_rotation[i])
            actual = disks[disk_order[i]][temp]
            actual = subtract(actual, disk_rotation[i])

        actual = connector_start[actual]



        # Back through plugboard
        actual = char_num(plugboard[num_char(actual)])

        result += num_char(actual)

        disk_rotation = rotate_disk(disk_rotation)

    else:
        result += letter

with open("output.txt", "w") as f:
    f.write(result)

print("------------ Result ------------")
print(result)
print("--------------------------------")

print("exiting, output saved on output.txt")
