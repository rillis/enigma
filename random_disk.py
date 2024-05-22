import random, os
import string

dict_letters = string.ascii_letters+string.digits+string.punctuation+' '
li = ['disk0.enigma', 'disk1.enigma', 'disk2.enigma', 'disk3.enigma', 'disk4.enigma', 'diskI.enigma', 'diskF.enigma']

def createDisks(folder, l):
    if not os.path.isdir(folder):
        os.mkdir(folder)

    for disk in li:
        if not os.path.isfile(f"{folder}/"+disk):
            d = {}
            poss = list(range(l))
            for x in range(l):
                indice = random.randint(0, len(poss) - 1)
                item = poss.pop(indice)
                d[x] = item
            with open(f"{folder}/"+disk, "w") as f:
                f.write(str(d))
            print(f"{folder}/"+disk, "created")
        else:
            print(f"{folder}/"+disk, "already exists")

createDisks("disks", len(string.ascii_lowercase))
createDisks("disks_special", len(dict_letters))
print("done.")