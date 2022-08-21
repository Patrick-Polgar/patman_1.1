import pygame
import math
import random
from pygame import mixer

pygame.init()

small_font = pygame.font.SysFont("Chiller", 35)
medium_font = pygame.font.SysFont("Chiller", 75)
big_font = pygame.font.SysFont("Chiller", 150)


def print_big(my_str, color, str_x, str_y):
    str_x = int(str_x)
    str_y = int(str_y)
    mytext = big_font.render(my_str, 1, color)
    screen.blit(mytext, (str_x, str_y))


def print_med(my_str, color, str_x, str_y):
    str_x = int(str_x)
    str_y = int(str_y)
    mytext = medium_font.render(my_str, 1, color)
    screen.blit(mytext, (str_x, str_y))


def print_small(my_str, color, str_x, str_y):
    str_x = int(str_x)
    str_y = int(str_y)
    mytext = small_font.render(my_str, 1, color)
    screen.blit(mytext, (str_x, str_y))


# global variables
# here we initialise all variables what we like to use to communicate between functions
size = 50
score = 0
half_size = int(size / 2)
width, height = 20 * size, 14 * size
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Patman - the best game ever")
pat_time = pygame.time.Clock()
FPS = 22
game_is_on = True

###################################################
# This list of string we use for building the map #
# We going to iterate trough to every line and than every charachter
map = [
    "XXXXXXXXXXXXXXXXX",
    "XP.....X      B X",
    "X XXXX.X XXXXX  X",
    "X......       G X",
    "X XX X XXX XX   X",
    "X XX       XX  XX",
    "X.XXXX XXX XX   X",
    "X.....          X",
    "XXXXX.XX X XX  XX",
    "X...X.X  X XX  XX",
    "X.....X  X    GXX",
    "XXXXXXXXXXXXXXXXX"
]


class Ball:
    def __init__(self, x, y):
        self.obj_name = "Ball"
        self.pic = pygame.transform.scale(pygame.image.load("Ball/0.png"), (int(size), int(size)))
        self.rect = self.pic.get_rect()
        self.rect.x, self.rect.y = x * size, y * size
        self.its_moving = False

    def draw(self):
        screen.blit(self.pic, self.rect)


class Wall:
    def __init__(self, x, y):
        self.obj_name = "Wall"
        self.pic = pygame.transform.scale(pygame.image.load("Wall/1.png"), (size, size))
        self.rect = self.pic.get_rect()
        self.rect.x, self.rect.y = x * size, y * size
        self.its_moving = False

    def draw(self):
        screen.blit(self.pic, self.rect)


# HERE IS ALL CREATURES IN GAME AS PACMAN AND GHOSTS
class Creatures:

    def __init__(self, x, y):
        self.obj_name = "Creatures"
        self.idx = 0
        self.max_idx = 0
        self.pic_list = []
        for pic in range(1):
            self.pic_list.append(pygame.transform.scale(pygame.image.load(f"Patman/0.png"), (size, size)))

        self.rect = self.pic_list[self.idx].get_rect()
        self.rect.x, self.rect.y = x * size, y * size
        self.speed = 10
        self.direction = [self.speed, 0]
        self.going_to = "right"
        self.its_moving = True

    def draw(self):
        # when we draw the object we need to check what way its facing to

        # checking for its moving right
        if self.direction == [self.speed, 0] or self.direction == [0, 0]:
            screen.blit(self.pic_list[self.idx], self.rect)
        # checking for its moving left
        if self.direction == [-self.speed, 0]:
            screen.blit(pygame.transform.flip(self.pic_list[self.idx], True, False), self.rect)
        # checking for its moving up
        if self.direction == [0, -self.speed]:
            screen.blit(pygame.transform.rotate(self.pic_list[self.idx], 90), self.rect)
        # checking for its moving down
        if self.direction == [0, self.speed]:
            screen.blit(pygame.transform.rotate(self.pic_list[self.idx], -90), self.rect)

        self.idx += 1
        if self.idx > self.max_idx:
            self.idx = 0

    # THIS IS CHECK THE CREATURES IN A MIDDLE OF THE GRID
    def Can_Turn(self):
        if self.rect.x % size == 0 and self.rect.y % size == 0:
            return True
        else:
            return False

    def no_wall(self, list_of_walls, direction_to_check):
        for wall in list_of_walls:
            if direction_to_check == "right":
                if self.rect.x + size == wall.rect.x and self.rect.y == wall.rect.y:
                    return False
            elif direction_to_check == "left":
                if self.rect.x - size == wall.rect.x and self.rect.y == wall.rect.y:
                    return False
            elif direction_to_check == "up":
                if self.rect.x == wall.rect.x and self.rect.y - size == wall.rect.y:
                    return False
            elif direction_to_check == "down":
                if self.rect.x == wall.rect.x and self.rect.y + size == wall.rect.y:
                    return False
        return True


#############################################
# here start all enemies code                #

class Enemy(Creatures):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.obj_name = "Enemy"
        self.max_idx = 8
        self.pic_list = []
        for pic in range(9):
            self.pic_list.append(
                pygame.transform.flip(pygame.transform.scale(pygame.image.load(f"Ghost/{pic}.png"), (size, size)), True,
                                      False))
        self.rect = self.pic_list[self.idx].get_rect()
        self.rect.x, self.rect.y = x * size, y * size
        self.speed = 5
        self.direction = [self.speed, 0]
        self.going_to = "right"

    # THIS IS JUST GIVE A RANDOM DIRECTION TO ENEMY
    def random_direction(self):
        direction = random.randint(1, 4)
        if direction == 1:
            self.going_to = "right"
            self.direction = [self.speed, 0]
        if direction == 2:
            self.going_to = "left"
            self.direction = [-self.speed, 0]
        if direction == 3:
            self.going_to = "up"
            self.direction = [0, -self.speed]
        if direction == 4:
            self.going_to = "down"
            self.direction = [0, self.speed]


class Blue_ghost(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.speed = 8
        self.pic_list = []

        for pic in range(9):
            self.pic_list.append(
                pygame.transform.flip(pygame.transform.scale(pygame.image.load(f"Blue_Ghost/{pic}.png"), (size, size)),
                                      True, False))


class Pacman(Creatures):
    def __init__(self, x, y):
        super().__init__(x, y)

        self.obj_name = "Patman"
        self.max_idx = 8
        self.pic_list = []
        for pic in range(9):
            self.pic_list.append(pygame.transform.scale(pygame.image.load(f"Patman/{pic}.png"), (size, size)))
        self.rect = self.pic_list[self.idx].get_rect()
        self.rect.x, self.rect.y = x * size, y * size
        self.speed = 10
        self.direction = [self.speed, 0]
        self.going_to = "right"


#########################################################
# this function is going to draw everything into screen  #
def draw_all(list_of_obj):
    for this_obj in list_of_obj:
        this_obj.draw()


def refresh_screen():
    print_small(f"score: {score}", (220, 220, 220), size * 17, size * 2)
    # update everything into screen
    pygame.display.update()
    # delay for make the graphic seeable
    pat_time.tick(FPS)
    # this is just going to
    screen.fill((0, 0, 0))


# here is going to all user input
def user_input(patman):
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                global game_is_on
                game_is_on = False
            elif event.key == pygame.K_LEFT:
                patman.direction = [-patman.speed, 0]
                patman.going_to = "left"

            elif event.key == pygame.K_RIGHT:
                patman.direction = [patman.speed, 0]
                patman.going_to = "right"

            elif event.key == pygame.K_UP:
                patman.direction = [0, -patman.speed]
                patman.going_to = "up"

            elif event.key == pygame.K_DOWN:
                patman.direction = [0, patman.speed]
                patman.going_to = "down"


#####################################
# HERE WE MOVE EVERYTHING ON SCREEN #
# obj_list = object list
def move_objects(obj_list):
    # make a list for walls
    list_of_walls = []
    for this_obj in obj_list:
        if this_obj.obj_name == "Wall":
            list_of_walls.append(this_obj)
        if this_obj.obj_name == "Patman":
            patman_x, patman_y = this_obj.rect.x, this_obj.rect.y

    global width, height, size
    for this_obj in obj_list:
        # check: Do we want to move this obj?
        if this_obj.its_moving:
            old_x, old_y = this_obj.rect.x, this_obj.rect.y

            if (this_obj.rect.x + this_obj.direction[0]) < width - size and this_obj.rect.x + this_obj.direction[0] > 0:
                this_obj.rect.x += this_obj.direction[0]
            if (this_obj.rect.y + this_obj.direction[0]) < height - size and this_obj.rect.y + this_obj.direction[
                0] > 0:
                this_obj.rect.y += this_obj.direction[1]
            for this_wall in list_of_walls:
                if this_wall.rect.colliderect(this_obj.rect):
                    # this_obj.direction = [0,0]

                    if this_obj.obj_name == "Enemy":
                        this_obj.random_direction()

                    if half_size > old_x - int(old_x / size) * size:
                        old_x = int(old_x / size) * size
                    else:
                        old_x = int(old_x / size) * size + size

                    if half_size > old_y - int(old_y / size) * size:
                        old_y = int(old_y / size) * size
                    else:
                        old_y = int(old_y / size) * size + size

                    # this_obj.going_to = "stay"
                    this_obj.rect.x, this_obj.rect.y = old_x, old_y


##############################################
# COLLUSION CHECK
# it is checking pacman encounter with ghost or ball...etc
def collusion_check(all_obj):
    for pat_obj in all_obj:
        if pat_obj.obj_name == "Patman":
            for this_obj in all_obj:
                if this_obj.obj_name == "Ball" and this_obj.rect.colliderect(pat_obj.rect):
                    all_obj.remove(this_obj)
                    global score
                    score += 1

                if this_obj.obj_name == "Enemy" and this_obj.rect.colliderect(pat_obj.rect):
                    global game_is_on
                    game_is_on = False


# game loop
def game_loop():
    all_obj = []

    global map
    wx, wy = 0, 0

    ###############################################################
    # build map based on list of strings, what name is as "map"   #

    for row in map:
        for char in row:
            if char == "X":
                all_obj.append(Wall(wx, wy))
            elif char == "G":
                all_obj.append(Enemy(wx, wy))
            elif char == "B":
                all_obj.append(Blue_ghost(wx, wy))
            elif char == "P":
                all_obj.append(Pacman(wx, wy))
            elif char == ".":
                all_obj.append(Ball(wx, wy))
            wx += 1
        wy += 1
        wx = 0


    # Call in sound files and play background music
    pygame.mixer.music.load("Sounds/ghost_song.mp3")
    pygame.mixer.music.play(-1)


    global game_is_on
    while game_is_on:

        # ask for user input and modify global variables
        for obj in all_obj:
            if obj.obj_name == "Patman":
                user_input(obj)

        # move objects
        move_objects(all_obj)

        # COLLUSION CHECK
        # it is checking pacman encounter with ghost or ball...etc
        collusion_check(all_obj)

        # draw all
        draw_all(all_obj)

        # clear screen
        refresh_screen()

        ## added new codes here ##
        # if Ball == [0]:
        #   global game_winner
        #   game_is_on = False
        #   game_winner = True

        # pygame.display.update()
        # pat_time.tick(FPS)   ## these codes cause vibration on the screen, I don't understand, why? ##


def game_is_over():
    global score
    screen.fill((0, 0, 0))
    print_big("Game over", (220, 220, 220), size * 4, size * 2)
    print_med(f"Score: {score}", (220, 220, 220), size * 8, size * 6)
    pygame.display.update()
    ## Added here " GAME OVER " music ##
    pygame.mixer.music.load("Sounds/Game_Over.mp3")
    pygame.mixer.music.play()
    for i in range(7):
        pat_time.tick(1)

## added this lines here to create winner option ##
def game_winner():
    global score
    screen.fill((0, 0, 0))
    print_big("You are the winner", (220, 220, 220), size * 4, size * 2)
    print_med(f"Score: {score}", (220, 220, 220), size * 8, size * 6)
    pygame.display.update()
    pygame.mixer.music.load("Sounds/Winner_sound.mp3")
    pygame.mixer.music.play()
    for i in range(10):
        pat_time.tick(1)



game_loop()
game_is_over()
pygame.quit()
quit()


## trying here, is not working ##
##    if Ball == 0:
##       game_winner = true

