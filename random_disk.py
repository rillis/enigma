import random, os


li = ['disk0.enigma', 'disk1.enigma', 'disk2.enigma', 'disk3.enigma', 'disk4.enigma', 'diskI.enigma', 'diskF.enigma']

if not os.path.isdir("disks"):
    os.mkdir("disks")

for disk in li:
    if not os.path.isfile("disks/"+disk):
        d = {}
        poss = list(range(26))
        for x in range(26):
            indice = random.randint(0, len(poss) - 1)
            item = poss.pop(indice)
            d[x] = item
        with open("disks/"+disk, "w") as f:
            f.write(str(d))
        print(disk, "created")
    else:
        print(disk, "already exists")

print("done.")