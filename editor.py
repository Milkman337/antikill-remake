from pyray import *
from raylib import IsKeyDown
from engine import *
import simpleJDB


class tile:
    def __init__(self, position, num: int) -> None:
        self.position = position
        self.num = num


class texture_level:
    def __init__(self, number: int, texture) -> None:
        self.number = number
        self.texture = texture


def main():
    width: int = 1280
    height: int = 720
    fullscreen: bool = False

    # set_config_flags(4)

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

    sel_block = 0

    scroll = Vector2(0, 0)

    level = dt.getkey("level")
    nums_gotten = []
    for num in level:
        if num in nums_gotten:
            pass
        else:
            loaded = load_texture("data/tiles/" + str(num) + ".png")
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
        pos = Vector2(i * TILESIZE, b * TILESIZE)
        newtile = tile(pos, num)
        level_tiles.append(newtile)

    set_target_fps(60)
    while not window_should_close():
        virtual_mousepos = Vector2(get_mouse_position().x / 8 + scroll.x, get_mouse_position().y / 8 + scroll.y)
        # ---update stuff---

        if (IsKeyDown(KeyboardKey.KEY_W)):
            scroll.y -= 2
        if (IsKeyDown(KeyboardKey.KEY_S)):
            scroll.y += 2
        if (IsKeyDown(KeyboardKey.KEY_A)):
            scroll.x -= 2
        if (IsKeyDown(KeyboardKey.KEY_D)):
            scroll.x += 2

        if (is_key_pressed(KeyboardKey.KEY_E)):
            sel_block += 1
        if (is_key_pressed(KeyboardKey.KEY_Q)):
            sel_block -= 1

        begin_texture_mode(target)
        clear_background(BLACK)
        for level_tile in level_tiles:
            if (
                level_tile.position.x - scroll.x < -TILESIZE or level_tile.position.y - scroll.y < -TILESIZE or level_tile.position.x - scroll.x > gamescreenwidth or level_tile.position.y - scroll.y > gamescreenheight):
                pass
            else:
                for texture in Level_textures:
                    if (level_tile.num == texture.number):
                        text_ = texture.texture
                draw_texture(text_, int(level_tile.position.x) - int(scroll.x),
                             int(level_tile.position.y) - int(scroll.y), WHITE)

        if (is_mouse_button_down(MouseButton.MOUSE_BUTTON_LEFT)):
            for level_tile in level_tiles:
                if (
                    level_tile.position.x - scroll.x < -TILESIZE or level_tile.position.y - scroll.y < -TILESIZE or level_tile.position.x - scroll.x > gamescreenwidth or level_tile.position.y - scroll.y > gamescreenheight):
                    pass
                else:
                    if (
                        virtual_mousepos.x > level_tile.position.x and virtual_mousepos.x < level_tile.position.x + TILESIZE and virtual_mousepos.y > level_tile.position.y and virtual_mousepos.y < level_tile.position.y + TILESIZE):
                        level_tile.num = sel_block

        # draw_fps(0, 0)

        for texture in Level_textures:
            if (sel_block == texture.number):
                text__ = texture.texture
        draw_texture(text__, 0, 0, WHITE)

        end_texture_mode()

        begin_drawing()
        draw_texture_pro(target.texture, Rectangle(0, 0, target.texture.width, -target.texture.height),
                         Rectangle(0, 0, 1280, 720), Vector2(0, 0), 0.0, WHITE)

        end_drawing()

    new_data = []
    for level_tile in level_tiles:
        new_data.append(level_tile.num)

    dt.setkey("level", new_data)


if __name__ == "__main__":
    main()
