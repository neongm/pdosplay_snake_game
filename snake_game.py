import msvcrt
from dosplay import Screen
from time import time, sleep
from random import randint
from threading import Thread
scr = Screen(80, 25)
scr.setup_size()

#----------------------- config -----------------------#
key_buffer = 'left'
speed = 0.1
food='*'
food_x=0
food_y=0
#------------------------------------------------------#

class Snake:
    def __init__(self, snake_length,x,y, border_x, border_y):
        self.snake_length = snake_length
        self.x = x
        self.y = y
        self.border_x = border_x
        self.border_y = border_y
        self.snake=[(x, y)]

    def move(self, dir):
        if dir == 'up':
            self.y-=1
        elif dir == 'down':
            self.y+=1
        elif dir == 'right':
            self.x+=1
        elif dir == 'left':
            self.x-=1

        if self.x >= self.border_x: self.x = 0
        elif self.y >= self.border_y: self.y = 0
        elif self.y <= 0: y = self.border_y
        elif self.x <= 0: x = self.border_x

        self.snake.append((self.x, self.y))
        if scr.vram[self.x+self.y*scr.xsize]==food:
            self.snake_length+=1
            food_generator()
        if len(self.snake) > self.snake_length: del self.snake[0]

    def death(self):
        for i in range(len(self.snake)-1):
            if self.snake[i]==self.snake[-1]: return True
        return False

    def iswin(self):
        if self.snake_length==scr.xsize-1*scr.ysize-1: return True

    def vin_snake(self):
        for i in self.snake:
            scr.vin('@',i[0],i[1])


def ars():
    global key_buffer
    while True:
        k = msvcrt.getch()
        if k == b'K' and key_buffer != 'right':  key_buffer='left'
        elif k == b'H' and key_buffer != 'down':  key_buffer = 'up'
        elif k == b'M' and key_buffer != 'left':  key_buffer = 'right'
        elif k == b'P' and key_buffer != 'up':  key_buffer = 'down'


def food_generator():
    global food_x
    global food_y
    while True:
        x = randint(0, scr.xsize-1)
        y = randint(0, scr.ysize-2)
        if scr.vram[y*scr.xsize+x]==' ':
            food_x = x
            food_y = y
            break

def replay():
    main()

def main():
    global food_y
    global food_x
    global key_buffer
    snk = Snake(3, 10, 10, scr.xsize-1, scr.ysize-1)
    food_generator()
    frame = 0
    t = Thread(target=ars)  # keyboard
    t.start()
    while True:
        frame+=1
        scr.clear_vram()
        scr.vin(food, food_x, food_y)
        scr.vin(str(key_buffer),0,0)
        scr.vin(str(frame), 0, 1)
        scr.vin(str(snk.snake_length), 0, 2)
        if snk.death(): break
        if snk.iswin():
            scr.vin('0w0, you did it, omg',30,9)
            break
        snk.move(key_buffer)
        snk.vin_snake()
        scr.render()
        sleep(speed)
    scr.vin('game over',40,10)
    scr.vin('score: {}'.format(snk.snake_length-3), 40, 11)
    scr.render()
    sleep(2)
    replay()



main()
