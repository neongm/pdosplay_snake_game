import os
class Screen():
    def __init__(self, xsize, ysize):
        self.xsize = xsize
        self.ysize = ysize
        self.vram = [' ' for i in range(xsize*ysize+1)]
        self.vram_length = len(self.vram)-1

    def setup_size(self): os.system("mode con cols={} lines={}".format(self.xsize, self.ysize+2))

    def vin(self, string, x, y):
        index = y*self.xsize+x
        if len(string)==1 and index<self.vram_length:
            self.vram[index] = string
        else:
            for i in range(len(string)):
                ind = index + i
                if ind < self.vram_length:
                    self.vram[ind] = string[i]

    def clear_vram(self): self.vram = [' ' for i in range(self.xsize*self.ysize+1)]

    def render(self): print(''.join(self.vram))
