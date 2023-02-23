from pyray import *
import math

def distance(position_one: Vector2, position_two: Vector2):
    one = position_one.x - position_two.x
    two = position_one.y - position_two.y

    three = one * one
    four = two * two

    five = three + four
    return math.sqrt(five)

def addglow(position: Vector2, r: float, amount: int, color: Color):
    begin_blend_mode(BlendMode.BLEND_ADD_COLORS)

    for i in range(amount+1):
        draw_circle(int(position.x), int(position.y), r+(r*i), Color(int(color.r/17), int(color.g/17), int(color.b/17), int(color.a/17)))

    end_blend_mode()

def removeglow():
    begin_blend_mode(BlendMode.BLEND_SUBTRACT_COLORS)

    draw_rectangle(0, 0, 1920, 1080, Color(20, 20, 20, 20))

    end_blend_mode()

LIGHTGRAY = Color(200, 200, 200, 255)
GRAY = Color(130, 130, 130, 255)
DARKGRAY = Color(80, 80, 80, 255)
YELLOW = Color(253, 249, 0, 255)
GOLD = Color(255, 203, 0, 255)
ORANGE = Color(255, 161, 0, 255)
PINK = Color(255, 109, 194, 255)
RED = Color(230, 41, 55, 255)
MAROON = Color(190, 33, 55, 255)
GREEN = Color(0, 228, 48, 255)
LIME = Color(0, 158, 47, 255)
DARKGREEN = Color(0, 117, 44, 255)
SKYBLUE = Color(102, 191, 255, 255)
BLUE = Color(0, 121, 241, 255)
DARKBLUE = Color(0, 82, 172, 255)
PURPLE = Color(200, 122, 255, 255)
VIOLET = Color(135, 60, 190, 255)
DARKPURPLE = Color(112, 31, 126, 255)
BEIGE = Color(211, 176, 131, 255)
BROWN = Color(127, 106, 79, 255)
DARKBROWN = Color(76, 63, 47, 255)
WHITE = Color(255, 255, 255, 255)
BLACK = Color(0, 0, 0, 255)
BLANK = Color(0,0,0,0)
MAGENTA = Color(255, 0, 255, 255)
RAYWHITE = Color(245, 245, 245, 255)