import os
import string
import sys

dict_letters = string.ascii_letters+string.digits+string.punctuation+' '

def add(x, y):
    return (x + y) % len(dict_letters)


def subtract(x, y):
    return (x - y + len(dict_letters)) % len(dict_letters)

def char_num(letter):
    return dict_letters.index(letter)


def num_char(num):
    return dict_letters[num]


def configure_plugboard(pc):
    pb = {}
    for x in pc:
        pb[x] = pc[x]
        pb[pc[x]] = x
    for x in dict_letters:
        if x not in pb:
            pb[x] = x
    return pb


def invert_mapping(mapping):
    return {v: k for k, v in mapping.items()}


def rotate_disk(disk):
    new_disk = [disk[0], disk[1], disk[2]]
    new_disk[0] += 1
    if new_disk[0] >= len(dict_letters):
        new_disk[0] = 0
        new_disk[1] += 1
    if new_disk[1] >= len(dict_letters):
        new_disk[1] = 0
        new_disk[2] += 1
    if new_disk[2] >= len(dict_letters):
        new_disk[2] = 0
    return new_disk


def inverse_disks(disks):
    return [{v: k for k, v in disk.items()} for disk in disks]


# ------------ start "constants"
# random generated disks
for x in ['disk0.enigma', 'disk1.enigma', 'disk2.enigma', 'disk3.enigma', 'disk4.enigma', 'diskI.enigma',
          'diskF.enigma']:
    if not os.path.isfile("disks_special/" + x):
        print("Disks not generated/loaded, please run random_disks.py")
        sys.exit()

disks = []
for disk_n in range(5):
    with open(f'disks_special/disk{disk_n}.enigma', 'r') as f:
        disks.append(eval(f.read()))

with open(f'disks_special/diskI.enigma', 'r') as f:
    connector_start = eval(f.read())
with open(f'disks_special/diskF.enigma', 'r') as f:
    connector_end = eval(f.read())

# ------------ config
disk_order = None
plugboard_config = None
disk_rotation = None
with open('config.cfg', 'r') as file:
    lines = file.readlines()
for line in lines:
    exec(line)

disks = inverse_disks(disks)
connector_start = invert_mapping(connector_start)
connector_end = invert_mapping(connector_end)

# ------------ run
plugboard = configure_plugboard(plugboard_config)

complete_input = input("-> ")
result = ""

for letter in complete_input:
    if letter in dict_letters:
        actual = char_num(letter)

        # Through plugboard
        actual = char_num(plugboard[num_char(actual)])

        # Reverse the order for decrypt
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
