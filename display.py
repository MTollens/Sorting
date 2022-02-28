import pygame
# import math
import random
import colorsLib as color
# import math
# import colour as colour

pygame.init()
smalltext = pygame.font.Font("SCR.otf", 17)
step_enable = False

class Enviroment():
    def __init__(self, display_width, display_height, fps, caption=None, add_vars=None):

        # the pixel width of the window
        self.display_width = display_width

        # the pixel height of the window
        self.display_height = display_height

        #pygame clock
        self.clock = pygame.time.Clock()

        # the gamedisplay object
        self.gameDisplay = pygame.display.set_mode((display_width, display_height))

        # frames per second
        self.fps = fps

        # additional variables
        self.vars = add_vars

        # the caption on the window
        if not caption:
            caption = "no caption found"
        self.caption = ""
        self.update_caption(caption)

    # takes a string and applies it as the window text, saved in a variable for reference
    def update_caption(self, string=None):
        if string:
            self.caption = str(string)
        pygame.display.set_caption(self.caption)

    def resize_event(self, update):
        self.display_width = update[0]
        self.display_height = update[1]
        self.update_caption()

    # display dimenstions, returns a two item tuple, with: (width, height)
    # takes an optional argument to assign the width instead of return it
    def display_dims(self, update=None):
        if isinstance(update, list):
            if isinstance(update[0], int):
                if isinstance(update[1], int):
                    self.display_width = update[0]
                    self.display_height = update[1]
        return (self.display_width, self.display_height)


Env = Enviroment(1200, 800, 120, 'sorter')


class Objects():
    #comparisons, vs array accesses
    draw_buckets = False
    buckets = [0,0, 0,0, 0,0, 0,0, 0,0]
    class Tile():
        def __init__(self, value, color):
            self.value = value
            self.color = color

        # position is the horizontal coordinate of the draw rect, gamedisplay is where to draw
        def draw(self, pos, gameDisplay, display_height, tiles, color_override=None):
            width = (Env.display_width / tiles)
            #
            height = (tiles - self.value - 1) * (display_height/tiles)
            # this version changes the slope to be the other direction
            #height = self.value * (display_height / tiles)
            if color_override:
                draw_color = color_override
            else:
                draw_color = self.color
            #pygame.draw.rect(gameDisplay, self.color, [self.value, pos*length, width, 10])
            pygame.draw.rect(gameDisplay, draw_color, [pos-2, height, width+2, display_height])

        def __repr__(self):
            # return "tile:[{},{}]".format(self.color, self.value)
            return "tle{}".format(self.value)

    def __init__(self, tiles, color1=None, color2=None, color3=None, color4=None):
        if not color1:
            color1 = color.RC()

        if not color2:
            color2 = color.RC()

        # a list of what items have been checked this last cycle
        # key:
        # red tiles are being compared
        self.compared = [None, None, None]  # draws red
        self.focus = [None, None, None]     # draws green
        self.hold = [None, None, None]      # draws dark blue

        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
        self.color4 = color4

        self.regenerate(tiles)
        
    def color_between(self, color1, color2, start, end, index, offset=0):
        next_color = list(color.black)
        if index == start:
            next_color = color1
        elif index == end:
            next_color = color2
        else:
            # color2 = color.square_root(color2)
            # color1 = color.square_root(color1)
            for c in [0, 1, 2]:
                temp = abs((((color1[c] - color2[c])) / end) * (index-offset))
                print("({} / {}) * {}   =  {}".format((color1[c] - color2[c]), end, index-offset, temp))
                # print("{} {} --> {}".format(end, index-offset, temp))
                # print(temp)
                if color1[c] >= color2[c]:
                    next_color[c] = (int(color1[c] - temp))
                else:
                    next_color[c] = (int(color1[c] + temp))

                if next_color[c] < 0:
                    next_color[c] = 0
                elif next_color[c] > 255:
                    next_color[c] = 255

        # print("x = {}: color = ({},{},{})".format(x, next_color[0], next_color[1], next_color[2]))
        return next_color

    # runs the regenerate sequence,
    def regenerate(self, tiles):
        self.number_of_tiles = tiles
        # the actual list of items
        self.items = [0] * self.number_of_tiles

        # generate the colors
        # dynamically generates a gradient between the two given colors
        if self.color3 == None:
            for x in range(0, self.number_of_tiles):
                self.items[x] = Objects.Tile(x, self.color_between(self.color1, self.color2, 0, self.number_of_tiles, x))
        elif self.color4 == None:
            halfway = int(self.number_of_tiles/2)
            for x in range(0, halfway):
                self.items[x] = Objects.Tile(x, self.color_between(self.color1, self.color2, 0, halfway, x))
            # color2 = self.color_between(self.color1, self.color2, 0, halfway, halfway)
            for x in range(halfway, self.number_of_tiles):
                self.items[x] = Objects.Tile(x, self.color_between(self.color2, self.color3, halfway, self.number_of_tiles, x, halfway))
        else:
            thirdway = int(self.number_of_tiles*.3333)
            twothird = int(self.number_of_tiles*.6666)
            for x in range(0, thirdway):
                self.items[x] = Objects.Tile(x, self.color_between(self.color1, self.color2, 0, thirdway, x))
            for x in range(thirdway, twothird):
                self.items[x] = Objects.Tile(x, self.color_between(self.color2, self.color3, thirdway, twothird, x, thirdway))
            for x in range(twothird, self.number_of_tiles):
                self.items[x] = Objects.Tile(x, self.color_between(self.color3, self.color4, twothird, self.number_of_tiles, x, twothird))
        #
        # for x in self.items:
        #     # print(x.color)
        #     # print(color.luma(x.color))

    def shuffle(self):

        #this block it to check and make sure that the input and output contain the same elements
        beforesum = 0
        for x in self.items:
            beforesum += x.value

        first_number = random.randint(0, self.number_of_tiles-1)
        second_number = random.randint(0, self.number_of_tiles-1)
        while first_number == second_number:
            second_number = random.randint(0, self.number_of_tiles-1)


        temp = self.items[first_number]
        self.items[first_number] = self.items[second_number]
        self.items[second_number] = temp

        del temp

        # this block checks the other side of a one term shuffle
        aftersum = 0
        for x in self.items:
            aftersum += x.value

        # a term was lost or gained somewhere in the shuffle
        if aftersum != beforesum:
            print("critical failure!")

    def draw(self, gameDisplay, display_dims):
        display_height = display_dims[1]
        display_width = display_dims[0]
        for x in range(0, len(self.items)):
            draw_color = None
            if not self.items[x]:
                continue
            if x in self.compared:
                draw_color = color.red
            elif x in self.focus:
                draw_color = color.green
            elif x in self.hold:
                draw_color = color.blue

            self.items[x].draw((x * (display_width / self.number_of_tiles)), gameDisplay, display_height,
                               self.number_of_tiles, draw_color)

        self.compared = [None, None, None]      # draws red
        self.focus = [None, None, None]         # draws green
        self.hold = [None, None, None]          # draws dark blue

        if self.draw_buckets:
            for x in range(0, 10):
                pygame.draw.rect(Env.gameDisplay, color.white, [x*(Env.display_width / 10)+30, Env.display_height -100, 50, 25])
                disp_text(str(self.buckets[x]), (x*(Env.display_width / 10) + 55, Env.display_height -85))

    def get_item(self, index):
        return self.items[index]

    def swap_elements(self, element_1, element_2):
        temp = self.items[element_1]
        self.items[element_1] = self.items[element_2]
        self.items[element_2] = temp

    def single_item_sort(self, item_number):
        # returns true if a single item is sorted
        return self.items[item_number] == self.items[item_number].value

    def truesort(self):
        # this is a real sorted test, no funny business
        problems = False

        # runs down the list, compares the value to its indice in the list, because of the way this is written
        # a correctly sorted list will have tiles that contain the value of their position in the list
        for x in range(0, len(self.items)):
            if x != self.items[x].value:
                problems = True
                break

            #print("X:{}, value:{}".format(x, self.items[x].value))

        return not(problems)

    def ordersort(self):
        #this may need to be modified, or duplicated + modified for some of the sorts
        return False

    def printout(self):
        string = ""
        for x in self.items:
            string += str(x.value) + " "
        print(string)


def disp_text(text, location=None, hue=None):

    #generates a text surface that is a rect object with the given text on it
    def text_objects(text, font, hue=None):
        if not hue:
            hue = color.black
        textsurface = font.render(text, True, hue)
        return textsurface, textsurface.get_rect()
    TextSurf, TextRect = text_objects(text, smalltext, hue)
    if not location:
        TextRect.center = ((Env.display_width / 2), (Env.display_height / 2))
    else:
        TextRect.center = (location[0], location[1])
    Env.gameDisplay.blit(TextSurf, TextRect)


class Bubblesort():
    """
    Bubblesort, named because values float like bubbles towards their correct position
    very ineficcient, mostly used as a learning tool
    works by comparing every indice to its neighbor and swapping them if the swap results in a correct config
    """
    def __init__(self):
        self.rounds = 1
        self.offset = 0
        self.clean_passes = 0

    def sort(self, objs):
        assert isinstance(objs, Objects), "not an Objects class instance"
        pygame.draw.rect(Env.gameDisplay, color.white, [(Env.display_width / 2) - 75, 60, 150, 25])
        disp_text("Bubble sort", (Env.display_width / 2, 75))

        objs.compared = [self.offset + 1, self.offset]

        self.offset += 1
        if self.offset == objs.number_of_tiles - self.rounds:
            self.offset = 0
            self.rounds += 1
            if self.clean_passes >= 1:
                self.clean_passes = 2
            else:
                self.clean_passes = 1

        if objs.items[self.offset].value > objs.items[self.offset + 1].value:
            objs.swap_elements(self.offset, self.offset + 1)
            self.clean_passes = 0


        return objs, self.clean_passes >= 2


class Quicksort():
    """
    Quicksort, a fast, fairly efficient algorithm
    used in real world
    works by recursivly subdividing the elements into greater than and less than a chosen pivot point, if this were run
    on an actual dataset, it would run recursivly, and could possibly be multithreaded

    """

    class Stack():
        # last in first out
        def __init__(self):
            self.__contents = []
            self.__items = 0

        def pop(self):
            temp = None
            if self.__items == 0:
                return temp
            temp = self.__contents[self.__items-1]
            del self.__contents[self.__items-1]
            self.__items -= 1
            return temp

        def peek(self):
            return self.__contents[self.__items-1]

        def push(self, item):
            self.__contents.append(item)
            self.__items += 1

        def isEmpty(self):
            return self.__items == 0

        def items(self):
            return self.__items

        def printout(self):
            string = "("
            for x in self.__contents:
                string += str(x) + ", "
            string += ")"
            print(string)


    def __init__(self):
        self.stage = 0
        # the indice value of each position
        self.pivot = None
        self.left = 0
        self.right = 0

        # used to determine when we should stop subdividing and start cleaning
        self.mode = 0
        self.pivotmoves = 0
        self.stage = 0

        # used to know when to stop
        self.clean_passes = 0

        # used to know where we need to return to to continue processing after a subdivision
        self.markers = Quicksort.Stack()

    def debug(self):
        print("X+X+X+X+X+X+X+X+X+X+X+X+X+X+X+X")
        print("left {}  pivot {}   right {}".format(self.left, self.pivot, self.right))
        print("stage {}   clean {}  mode {}".format(self.stage, self.clean_passes, self.mode))
        self.markers.printout()

    def sort(self, objs):
        finished = 0
        #print(self.mode)
        assert isinstance(objs, Objects), "not an Objects class instance"
        pygame.draw.rect(Env.gameDisplay, color.white, [(Env.display_width / 2) - 75, 60, 150, 25])
        disp_text("Quicksort", (Env.display_width / 2, 75))

        # this is the real INIT method, the other one is just so that there are class values that can be seen through time
        if self.stage == 0:
            self.stage = 1
            self.left = 0
            self.right = objs.number_of_tiles -1
            self.pivot = round(objs.number_of_tiles/2)

        #self.debug()

        # core loop below X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X

        if (objs.items[self.left].value <= objs.items[self.pivot].value):
            # in this case there is no issue, check the next value on the next cycle
            self.left += 1
            objs.compared = [self.left]
            objs.hold = [self.right]

        elif (objs.items[self.left].value > objs.items[self.pivot].value):
            # in this case the checked value is greater than the pivot, so we must do something about it
            objs.compared = [self.left, self.right]

            if objs.items[self.right].value >= objs.items[self.pivot].value:
                # the right object is also bigger than the pivot, so we move forward and check the next rightmost object
                self.right -= 1
            elif objs.items[self.right].value < objs.items[self.pivot].value:
                # the right most object is smaller than the pivot, and the left one is bigger, so we swap them
                objs.swap_elements(self.right, self.left)

        objs.focus = [self.pivot]
        if self.left < 3 and self.pivot < 3 and self.right < 3:
            self.mode = 1


        if self.left == self.right or (self.left == (self.right-1)):
            if (objs.items[self.left].value > objs.items[self.pivot].value) and (objs.items[self.right].value < objs.items[self.left].value):
                objs.swap_elements(self.right, self.left)
            if self.pivotmoves < objs.number_of_tiles*.1:
                self.left = 0
                self.right = objs.number_of_tiles - 1
                self.pivot = random.randint(self.left, self.right)
                self.pivotmoves += 1
            else:
                if self.stage == 0:
                    self.left = 0
                    self.right = objs.number_of_tiles - 1
                    self.pivot = 2
                    self.stage = 1
                else:
                    self.left = 0
                    self.right = objs.number_of_tiles - 1
                    self.pivot += 1
                    self.stage = 1
                if self.pivot <= objs.number_of_tiles/2:
                    self.right = self.pivot + 10
                    if self.pivot < objs.number_of_tiles and self.pivot > 12:
                        self.left = self.pivot - 10
                elif self.pivot > objs.number_of_tiles/2:
                    self.left = self.pivot - 10
                    if self.pivot < objs.number_of_tiles -20:
                        self.right = self.pivot +10


            finished = self.clean_passes
            # the two sides have found eachother, we now move the pivot
            #self.pivot += 1#int((self.left + self.right)/2)#+= random.randint(1, 2)
            if self.pivot >= objs.number_of_tiles-1:
                self.pivot = 0
                self.clean_passes += 1
                finished = self.clean_passes
                if self.clean_passes >= 3:
                    self.clean_passes = 0


        # core loop above X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X

        return objs, finished >=3


class CountingsortB10():
    position = 0
    power = 1
    empty = False
    def __init__(self):
        self.buckets = [[]] * 10
        # print(self.buckets)
        self.output = []

    def reset(self):
        self.buckets = [[]] * 10
        self.output = []

    def sort(self, objs):
        assert isinstance(objs, Objects), "not an Objects class instance"
        pygame.draw.rect(Env.gameDisplay, color.white, [(Env.display_width / 2) - 75, 60, 150, 25])
        disp_text("Counting B10", (Env.display_width / 2, 75))
        objs.draw_buckets = True
        # update the visual display
        for x in range(0, 9):
            objs.buckets[x] = len(self.buckets[x])

        if ((self.position < objs.number_of_tiles) and (self.empty == False)):
            # print(objs.number_of_tiles)
            objs.compared = [self.position]
            tile = objs.get_item(self.position)
            # if tile == None:
            #     # print("tile was none")
            #     return objs, False

            temp = "0000" + str(tile.value)
            # print(temp)
            val = int(temp[-1*self.power])
            # print("{} - > {} @  {}     {}".format(temp, val, self.position, self.empty))
            # bucket_items = len(self.buckets)
            # if bucket_items == 0:
            #     self.buckets[val] = [tile]
            # else:
            #     print(self.buckets)
            #     self.buckets[val] = [tile]
            self.buckets[val] = self.buckets[val] + [tile]

            self.position += 1
            # if self.position == 15:
            #     self.power += 1
            #     self.position = 0
            #     # print("EOP")
            #     # for x in range(0, 10):
            #     #     print(self.buckets[x])
            #     # print("EOP")
            # if self.power == 4:
            #     quitgame()
            return objs, False

        elif self.position >= objs.number_of_tiles:
            # print("ELSE")
            self.empty = True
            self.position = 0
            return objs, False

        if self.empty:
            # print("empty")
            for x in range(0,10):
                self.output = self.output + self.buckets[x]
            self.empty = False
            self.position = 0
            self.power += 1
            # print(objs.items)
            objs.items = self.output
            # print(objs.items)
            self.reset()
            if self.power >= 4:
                done = True
            else:
                done = False
            return objs, done


class CountingsortB2():
    position = 0
    power = 1
    empty = False
    def __init__(self):
        self.buckets = [[]] * 2
        # print(self.buckets)
        self.output = []
        self.one_found = False

    def reset(self):
        self.buckets = [[]] * 10
        self.output = []
        self.one_found = False

    def sort(self, objs):
        assert isinstance(objs, Objects), "not an Objects class instance"
        pygame.draw.rect(Env.gameDisplay, color.white, [(Env.display_width / 2) - 75, 60, 150, 25])
        disp_text("Counting B2", (Env.display_width / 2, 75))
        objs.draw_buckets = True
        # update the visual display
        for x in range(0, 2):
            objs.buckets[x] = len(self.buckets[x])

        if ((self.position < objs.number_of_tiles) and (self.empty == False)):
            # print(objs.number_of_tiles)
            objs.compared = [self.position]
            tile = objs.get_item(self.position)
            # if tile == None:
            #     # print("tile was none")
            #     return objs, False

            # currently this can count up to 1024
            temp = "0000000000" + '{:b}'.format(tile.value)
            # print(temp)
            val = int(temp[-1*self.power])
            if val == 1:
                self.one_found = True
            # print("{} - > {} @  {}     {}".format(temp, val, self.position, self.empty))
            # bucket_items = len(self.buckets)
            # if bucket_items == 0:
            #     self.buckets[val] = [tile]
            # else:
            #     print(self.buckets)
            #     self.buckets[val] = [tile]
            self.buckets[val] = self.buckets[val] + [tile]

            self.position += 1
            # if self.position == 15:
            #     self.power += 1
            #     self.position = 0
            #     # print("EOP")
            #     # for x in range(0, 10):
            #     #     print(self.buckets[x])
            #     # print("EOP")
            # if self.power == 4:
            #     quitgame()
            return objs, False

        elif self.position >= objs.number_of_tiles:
            # print("ELSE")
            self.empty = True
            self.position = 0
            return objs, False

        if self.empty:
            # print("empty")
            for x in range(0,2):
                self.output = self.output + self.buckets[x]
            self.empty = False
            self.position = 0
            self.power += 1
            # print(objs.items)
            objs.items = self.output
            # print(objs.items)
            if not self.one_found:
                done = True
            else:
                done = False
            self.reset()
            return objs, done


class Radixsort():
    pass


def quitgame():
    pygame.quit()
    quit()


def CreateWindow(width, height):
    # modified from: https://stackoverflow.com/questions/11603222/allowing-resizing-window-pygame/21248420#21248420
    '''Updates the window width and height '''
    global Display, display_width, display_height
    display_width = width
    display_height = height
    Display = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    Display.fill((255, 255, 255))


def finish_frame():
    pygame.display.update()  # shows all the things you have previously drawn ^^^^^
    Env.clock.tick(Env.fps)


def main_menu():
    leave = False
    while True:
        pygame.draw.rect(Env.gameDisplay, color.dark_red, [100, 100, 100, 100])
        for event in pygame.event.get():
            print(event)
            if leave:
                break
            elif event.type == pygame.VIDEORESIZE:
                CreateWindow(event.w, event.h)
                Env.display_dims((event.w, event.h))
                # print(str("{}, {}".format(display_width, display_height)))
            elif event.type == pygame.QUIT:
                quitgame()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    quitgame()
                if event.key == pygame.K_p:
                    leave = True
        if leave:
            break

        finish_frame()


def pause(objects):
    leave = False
    global step_enable
    objects.draw(Env.gameDisplay, Env.display_dims())
    while True:
        pygame.draw.rect(Env.gameDisplay, color.dark_red, [100, 100, 100, 100])
        disp_text("paused", (150, 150))
        for event in pygame.event.get():
            if leave:
                break
            elif event.type == pygame.VIDEORESIZE:
                CreateWindow(event.w, event.h)
                Env.display_dims((event.w, event.h))
                # print(str("{}, {}".format(display_width, display_height)))
            elif event.type == pygame.QUIT:
                quitgame()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    quitgame()
                elif event.key == pygame.K_p:
                    leave = True
                elif event.key == pygame.K_s:
                    leave = True
                elif event.key == pygame.K_e:
                    step_enable = False
                    leave = True
        if leave:
            break

        finish_frame()


def MainLoop():
    clear = True
    sorting_mode = False
    shuffle_mode = False
    shuffle_time = 0
    global step_enable
    bubble = Bubblesort()
    quick = Quicksort()
    counting = CountingsortB10()
    counting2 = CountingsortB2()
    # print(counting.buckets)
    algorithm = bubble
    # number of tiles is defined here, as the first variable in this function call
    # objects = Objects(400, color.light_blue, color.violet, color.red)
    objects = Objects(1024, color.item_yellow, color.orange, color.pink)
    # objects = Objects(30, color.white, color.black, color.white, color.black)
    while True:
        if sorting_mode and shuffle_mode:
            sorting_mode = False
            shuffle_mode = False
        if clear:
            Env.gameDisplay.fill(color.black)
        if step_enable:
            pause(objects)
        # get input
        for event in pygame.event.get():
            # window resize logic
            if event.type == pygame.VIDEORESIZE:
                CreateWindow(event.w, event.h)
                Env.resize_event((event.w, event.h))
                # print(str("{}, {}".format(display_width, display_height)))
            # window "X" pressed
            if event.type == pygame.QUIT:
                quitgame()
            # key pressed down logic
            if event.type == pygame.KEYDOWN:
                # graceful exit
                if event.key == pygame.K_LEFT:
                    quitgame()
                # disables screen clearing after each frame
                elif event.key == pygame.K_RIGHT:
                    clear = not clear
                # opens pause menu
                elif event.key == pygame.K_p:
                    pause(objects)
                elif event.key == pygame.K_s:
                    shuffle_mode = True
                elif event.key == pygame.K_t:
                    print(objects.truesort())
                elif event.key == pygame.K_b:
                    sorting_mode = True
                    objects.draw_buckets = False
                    algorithm = bubble
                elif event.key == pygame.K_c:
                    sorting_mode = True
                    algorithm = counting
                elif event.key == pygame.K_2:
                    sorting_mode = True
                    algorithm = counting2
                elif event.key == pygame.K_q:
                    sorting_mode = True
                    objects.draw_buckets = False
                    algorithm = quick
                elif event.key == pygame.K_e:
                    step_enable = not step_enable


        if sorting_mode and shuffle_mode:
            sorting_mode = False
            shuffle_mode = False


        # drawing
        objects.draw(Env.gameDisplay, Env.display_dims())

        if sorting_mode:
            #objects.printout()
            objects, finished = algorithm.sort(objects)
            if finished:
                objects.draw_buckets = False

            # algorithm.sort(objects)
            if finished:
                print("the objects class reports that the sorted status of the data is : {}".format(objects.truesort()))
                sorting_mode = False

        if shuffle_mode:
            pygame.draw.rect(Env.gameDisplay, color.dark_green, [(Env.display_width/2) -50, (Env.display_height/2) - 30, 100, 60])
            disp_text("Shuffling", (Env.display_width/2, Env.display_height/2))
            objects.shuffle()
            shuffle_time += 1
            if shuffle_time >= 2.5*objects.number_of_tiles:
                shuffle_mode = False
                shuffle_time = 0
        finish_frame()

if __name__ == "__main__":
    MainLoop()