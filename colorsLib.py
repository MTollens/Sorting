import random
# import math
light_grey = (200, 200, 200)
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
pink = (255,100,100)
dark_red= (200, 0, 0)
green = (0, 255, 0)
dark_green = (0, 200, 0)
blue = (0, 0, 255)
item_yellow = (236, 255, 145)
brown = (119, 77, 0)
light_brown = (173, 112, 0)
grey = (96, 96, 96)
orange = (255, 87, 8)
light_blue = (147, 255, 238)
dark_grey = (150,150,150)
violet = (116, 19, 196)


def muted(color):
    result = [0, 0, 0]
    result[0] = round(.75 * color[0])
    result[1] = round(.75 * color[1])
    result[2] = round(.75 * color[2])
    return result

def RC():
    result = [0, 0, 0]
    result[0] = random.randint(0, 255)
    result[1] = random.randint(0, 255)
    result[2] = random.randint(0, 255)
    return result

def square_root(item):
    item = list(item)
    for x in [0, 1,2]:
        print(item)
        item[x] = item[x]**(.5)
    return item

def square(item):
    item = list(item)
    for x in [0,1,2]:
        item[x] = item[x]**2
    return item

def luma(color):
    return (0.299*(color[0]**2) + 0.587*(color[1]**2) + 0.114*(color[2]**2))**.5

if __name__ == "__main__":
    print("a color library")