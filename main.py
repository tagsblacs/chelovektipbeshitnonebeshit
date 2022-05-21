from tkinter import *
import random as r
import time as t
class Game(object):
    def __init__(self):
        self.tk = Tk()
        self.tk.title("igra2")
        self.tk.resizable(0, 0)
        self.tk.wm_attributes("-topmost", 1)
        self.canvas_height = 1000
        self.canvas_width = 1000
        self.canvas = Canvas(self.tk, width = self.canvas_height, height = self.canvas_width)
        self.canvas.pack()
        self.tk.update()
        self.bg = PhotoImage(file="1.gif")
        w = self.bg.width()
        h = self.bg.height()
        def coords(self):
            xy = list(self.game.canvas.coords(self.image))
            self.coordinates.x1 = xy[0]
            self.coordinates.y1 = xy[1]
            self.coordinates.x2 = xy[0] + 300
            self.coordinates.y2 = xy[1] + 300
            return self.coordinates
            
        for x in range(0, 10):
            for y in range(0, 10):
                self.canvas.create_image(x*w, y*h, image=self.bg, anchor='nw')
        self.sprites = []
        self.running = True
    def mainloop(self):
        while 1:
            if self.running == True:
                for sprite in self.sprites:
                    sprite.move()
            self.tk.update_idletasks()
            self.tk.update()
            t.sleep(0.01)
class Coords(object):
    def __init__(self, x1=0, y1=0, x2=0, y2=0):
          self.x1 = x1
          self.y1 = y1
          self.x2 = x2
          self.y2 = y2
    def within_x(co1, co2):
        if (co1.x1 > co2.x1 and co1.x1 < co2.x2) \
            or (co1.x2 > co2.x1 and co1.x2 < co2.x2) \
            or (co2.x1 > co1.x1 and co2.x1 < co1.x2) \
            or (co2.x2 > co1.x1 and co2.x2 < co1.x2) :
            return True
        else:
            return False
    def within_y(co1, co2):
        if (co1.y1 > co2.y1 and co1.y1 < co2.y2) \
            or (co1.y2 > co2.y1 and co1.y2 < co2.y2) \
            or (co2.y1 > co1.y1 and co2.y1 < co1.y2) \
            or (co2.y2 > co1.y1 and co2.y2 < co1.y2) :
            return True
        else:
            return False
    def col_left(co1, co2):
        if within_y(co1, co2):
            if co1.x1 >= co2.x1 and co1.x1 <= co2.x2:
                return True
        return False
    def col_right(co1, co2):
        if within_y(co1, co2):
            if co1.x2 >= co2.x1 and co1.x2 <= co2.x2:
                return True
        return False
    def col_top(co1, co2):
        if within_x(co1, co2):
            if co1.y1 >= co2.y1 and co1.y1 <= co2.y2:
                return True
        return False
    def col_bottom(y, co1, co2):
        if within_x(co1, co2):
            y_calc = y + co1.y2
            if y_calc >= co2.y1 and y_calc <= co2.y2:
                return True
        return False
class Sprite(object):
    def __init__(self, game):
        self.game = game
        self.endgame = False
        self.coordinates = None
    def move(self):
        co = self.coords()
        left = True
        right = True
        top = True
        bottom = True
        falling = True
        if self.y > 0 and co.y2 >= self.game.canvas_height:
            self.y = 0
            bottom = False
        elif self.y < 0 and co.y1 <= 0:
            self.y = 0
            top = False
        if self.x > 0 and co.x2 >= self.game.canvas_width:
            self.x = 0
            right = False
        elif self.x < 0 and co.x1 <= 0:
            self.x = 0
            left = False
        for sprite in self.game.sprites:
            if sprite == self:
                continue
            sprite_co = sprite.coords()
            if top and self.y < 0 and col_top(co, sprite_co):
                self.y = -self.y
                top = False
            if bottom and self.y > 0 and col_bottom(self.y, co, sprite_co):
                self.y = sprite_co.y1 - co.y2
                if self.y < 0:
                   self.y = 0
                bottom = False
                top = False
            if bottom and falling and self.y == 0 and co.y2 < self.game.canvas_height and collided_bottom(1, co, sprite_co):
                falling = False
            if left and self.x < 0 and col_left(co, sprite_co):
                self.x = 0
                left = False
            if right and self.x > 0 and col_right(co, sprite_co):
                self.x = 0
                right = False
            if falling and bottom and self.y == 0 and co.y2 < self.game.canvas_height:
                self.y = 4
            self.game.canvas.move(self.image, self.x, self.y)
    def coords(self):
        return self.coordinates
class PlatformSprite(Sprite):
    def __init__(self, game, photo_image, x, y, width, height):
        Sprite.__init__(self, game)
        self.photo_image = photo_image
        self.image = game.canvas.create_image(x, y, image=self.photo_image, anchor="nw")
        self.coordinates = Coords(x, y, x + width, y + height)
class StickFigureSprite(Sprite):
    def __init__(self, game):
        Sprite.__init__(self, game)
        self.images_left = [PhotoImage(file="pers.gif"),
                            PhotoImage(file="pers1.gif"),
                            PhotoImage(file="pers2.gif")

        ]
        self.images_right = [PhotoImage(file="pers3.gif"),
                             PhotoImage(file="pers2.gif"),
                             PhotoImage(file="pers1.gif")
        ]
        self.image = game.canvas.create_image(200, 470, image=self.images_left[0], anchor='nw')
        #self.coordinates = Coords(x, y, x + width, y + height)
        self.jump_count = 0
        self.coordinates = Coords()
        self.current_image = 0
        self.current_image_add = 1
        self.x = -2
        self.y = 0
        self.last_time = t.time()
        game.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        game.canvas.bind_all('<KeyPress-Right>', self.turn_right)
        game.canvas.bind_all('<space>', self.jump)
    def turn_left(self, evg):
        self.x = -20
        print("233232")
    def turn_right(self, evg):
        self.x = 20
    def jump(self, evg):
        self.y = -40
    def animate(self):
        if self.x != 0 and self.y == 0:
            if t.time() - self.last_time > 0.1:
                self.last_time = t.time()
                self.current_image += self.current_image_add
                if self.current_image >= 2:
                    self.current_image_add = -1
                if self.current_image <= 0:
                    self.current_image_add = 1
    def move(self):
        self.animate()
        if self.y < 0:
            self.jump_count += 1
            if self.jump_count > 20:
                self.y = 40
        if self.y > 0:
            self.jump_count -= 1
        
j = Game()
platform1 = PlatformSprite(j, PhotoImage(file="platform1.gif"), 0, 800, 100, 10)
platform2 = PlatformSprite(j, PhotoImage(file="platform2.gif"), 300, 400, 300, 10)
platform3 = PlatformSprite(j, PhotoImage(file="platform3.gif"), 500, 200, 500, 10)
chelovek = StickFigureSprite(j)
sf = StickFigureSprite(j)
j.sprites.append(sf)
j.mainloop()
