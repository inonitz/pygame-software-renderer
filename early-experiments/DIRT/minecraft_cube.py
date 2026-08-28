import random
from Cube import Cube


def get_dirt():

    green1 = (105, 191, 90)
    green2 = (76, 153, 63)
    green3 = (118, 222, 100)

    green_list = (green1, green2, green3)

    brown1 = (79, 46, 26)
    brown2 = (99, 77, 55)
    brown3 = (148, 114, 80)

    brown_list = (brown1, brown2, brown3)

    grey = (142, 148, 156)

    dirt_block = []

    for y in range(8):
        layer = []
        for x in range(8):
            for z in range(8):
                if (x == 0 or z == 0) or y == 0 or (x == 7 or z == 7) or y == 7:
                    num = random.randint(0, 20)
                    if y == 0:
                        layer.append(Cube(x, y, z, 1, green_list[num % 3]))
                    elif 0 < y < 3:
                        if 0 <= num <= 10:
                            layer.append(Cube(x, y, z, 1, green_list[num % 3]))
                        else:
                            layer.append(Cube(x, y, z, 1, brown_list[num % 3]))
                    else:
                        if num == 10:
                            layer.append(Cube(x, y, z, 1, grey))
                        else:
                            layer.append(Cube(x, y, z, 1, brown_list[num % 3]))
        dirt_block.extend(layer)

    print(dirt_block)

    return dirt_block
