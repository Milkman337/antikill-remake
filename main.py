from pyray import *
from raylib import IsKeyDown
from engine import *
import simpleJDB
import random
import asyncio

collidabel_tiles = [
    1
]

class particle:
    def __init__(self, position, vel, active=False):
        self.time = 10
        self.position = position
        self.vel = vel
        self.active = active

    def update(self, dt):
        self.vel.y += 0.3 * dt
        self.time -= 1 * dt
        self.position.x += self.vel.x * dt
        self.position.y += self.vel.y * dt
        if self.time <= 0:
            self.active = False


    def draw(self):
        draw_circle(int(self.position.x), int(self.position.y), self.time/3, BLUE)

class tile:
    def __init__(self, position, num:int) -> None:
        self.position = position
        self.num = num

class texture_level:
    def __init__(self, number:int, texture) -> None:
        self.number = number
        self.texture = texture

class Player():
    def __init__(self, position: Vector2) -> None:
        self.position = position
        self.vel = Vector2(0,0)
        self.testpos = Vector2(0,0)
        self.rect = Rectangle(self.position.x -2, self.position.y -2, self.position.x +2, self.position.y +2)
        self.particles = []
        self.scroll = Vector2(0,0)
        for i in range(100):
            self.particles.append(particle(Vector2(0,0), Vector2(0,0)))


    def update(self, virtualmouse, level_tiles, TILESIZE, dt):
        for part in self.particles:
            if (part.active):
                part.update(dt)

        self.vel.y += 0.1 * dt
        if (self.vel.x != 0):
            self.vel.x /= 1.006
        self.position.x += self.vel.x * dt
        for tile in level_tiles:
            if tile.num in collidabel_tiles:
                if (self.position.x < tile.position.x + TILESIZE and self.position.x > tile.position.x and self.position.y < tile.position.y + TILESIZE and self.position.y > tile.position.y):
                    self.position.x -= self.vel.x
                    self.vel.x = self.vel.x*-1*0.3
        #if (self.position.x < 2 or self.position.x > 160-2):
        #    self.position.x -= self.vel.x
        #    self.vel.x = self.vel.x*-1*0.3
        self.position.y += self.vel.y * dt
        print(self.vel.y)
        for tile in level_tiles:
            if tile.num in collidabel_tiles:
                if (self.position.x < tile.position.x + TILESIZE and self.position.x > tile.position.x and self.position.y < tile.position.y + TILESIZE and self.position.y > tile.position.y):
                    self.position.y -=self.vel.y
                    self.vel.y = self.vel.y*-1*0.8
                    test = 0
                    for part in self.particles:
                        if (part.active):
                            test += 1
                    if (not(test > 1)):
                        for i in range(5):
                            for part in self.particles:
                                if part.active == False:
                                    part.position = Vector2(int(self.position.x)+int(self.scroll.x), int(self.position.y)+int(self.scroll.y))
                                    part.vel = Vector2(random.randint(-30,30)/10, random.randint(-30,30)/10)
                                    part.time = 10
                                    part.active = True
                                    break
        #if (self.position.y < 2 or self.position.y > 90-2):
        #    self.position.y -= self.vel.y
        #    self.vel.y = self.vel.y*-1*0.8


        test = Vector2(virtualmouse.x - (virtualmouse.x - self.position.x)*2, virtualmouse.y - (virtualmouse.y - self.position.y)*2)
        self.testpos = test

        if (is_mouse_button_pressed(MouseButton.MOUSE_BUTTON_LEFT)):
            test2 = Vector2(virtualmouse.x - self.position.x, virtualmouse.y - self.position.y)
            self.vel = Vector2(0,0)
            self.vel.x += test2.x/14
            self.vel.y += test2.y/14

    def draw(self, scroll: Vector2):
        self.scroll = scroll
        draw_circle(int(self.position.x)+int(scroll.x), int(self.position.y)+int(scroll.y), 3, BLUE)
        draw_line(int(self.position.x)+int(scroll.x), int(self.position.y)+int(scroll.y), int(self.testpos.x)+int(scroll.x), int(self.testpos.y)+int(scroll.y), RED)

        for part in self.particles:
            if (part.active):
                part.draw()

    def draw_lights(self):
        addglow(self.position, 30, 5, BLUE)

async def main():
    width = 1280
    height = 720
    fullscreen = False

    #set_config_flags(4)

    init_window(width, height, "pixelgame")
    init_audio_device()

    dt = simpleJDB.database("data/level")

    gamescreenwidth = 160
    gamescreenheight = 90
    LEVELWIDTH = dt.getkey("levelwidth")
    TILESIZE = dt.getkey("tilesize")

    target = load_render_texture(gamescreenwidth, gamescreenheight)
    set_texture_filter(target.texture, 0)

    level = []
    level_tiles = []
    Level_textures = []

    scroll = Vector2(8, 0)

    level = dt.getkey("level")
    nums_gotten = []
    for num in level:
        if num in nums_gotten:
            pass
        else:
            loaded = load_texture("data/tiles/"+str(num)+".png")
            newtext = texture_level(num, loaded)
            Level_textures.append(newtext)
            nums_gotten.append(num)

    i = -1
    b = 0
    for num in level:
        i += 1
        if (i == LEVELWIDTH):
            b += 1
            i = 0
        pos = Vector2(i*TILESIZE, b*TILESIZE)
        newtile = tile(pos, num)
        level_tiles.append(newtile)

    player = Player(Vector2(20,20))

    #set_target_fps(60)
    while not window_should_close():
        dt = get_frame_time()
        dt *= 65
        asyncio.sleep(0)
        virtual_mousepos = Vector2(get_mouse_position().x/8-scroll.x, get_mouse_position().y/8-scroll.y)
        # ---update stuff---

        player.update(virtual_mousepos, level_tiles, TILESIZE, dt)
        scroll.x += (-player.position.x-scroll.x +gamescreenwidth/2)/13 * dt
        scroll.y += (-player.position.y-scroll.y +gamescreenheight/2)/13 * dt

        #if (IsKeyDown(KeyboardKey.KEY_W)):
        #    scroll.y += 1
        #if (IsKeyDown(KeyboardKey.KEY_S)):
        #    scroll.y -= 1
        #if (IsKeyDown(KeyboardKey.KEY_A)):
        #    scroll.x += 1
        #if (IsKeyDown(KeyboardKey.KEY_D)):
        #    scroll.x -= 1

        print(player.position.x, player.position.y)

        begin_texture_mode(target)
        clear_background(BLACK)
        for level_tile in level_tiles:
            for texture in Level_textures:
                if (level_tile.num == texture.number):
                    text_ = texture.texture
            draw_texture(text_, int(level_tile.position.x) + int(scroll.x), int(level_tile.position.y) + int(scroll.y), WHITE)

        player.draw(scroll)

        #draw_text(f"{scroll.x}",0,20, 10, RAYWHITE)
        draw_fps(0, 0)
        end_texture_mode()

        begin_drawing()
        draw_texture_pro(target.texture, Rectangle(0, 0, target.texture.width, -target.texture.height), Rectangle(0, 0, 1280, 720), Vector2(0,0), 0.0, WHITE)

        end_drawing()

asyncio.run(main())