import directKeys
from directKeys import *
from PIL import ImageGrab, Image
import time


class Color:
    def __init__(self, r: int, g: int, b: int):
        self.r = r
        self.g = g
        self.b = b


class Vector2:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Food:

    coords: Vector2
    unique_color: Color

    def __init__(self, coords: Vector2, unique_color: Color):
        self.coords = coords
        self.unique_color = unique_color
    def throw_food(self, coords):
        directKeys.startDrag(self.coords.x, self.coords.y)
        directKeys.endDrag(coords)


class OrderZone:
    start = Vector2
    end = Vector2

    def __init__(self, start: Vector2, end: Vector2):
        self.start = start
        self.end = end

    def get_middle(self) -> Vector2:
        return Vector2(
            self.start.x + (self.end.x - self.start.x)/2,
            self.start.y + (self.end.y - self.start.y)/2
        )

    def check_for_color(self, color: Color) -> bool:
        screen = ImageGrab.grab()
        screen = screen.convert("RGB")
        for x in range(self.start.x, self.end.x):
            for y in range(self.start.y, self.end.y):
                r, g, b = screen.getpixel((x, y))
                pixel_color = Color(r, g, b)
                if pixel_color == color:
                    return True

        return False


# FOOD

chips = Food(Vector2(787, 509), Color(255, 105, 26))
tomato = Food(Vector2(705, 557), Color(252, 118, 99))
cheese = Food(Vector2(617, 557), Color(253, 215, 100))
salad = Food(Vector2(649, 484), Color(169, 182, 214))
sausage = Food(Vector2(530, 580), Color(244, 199, 189))
lettuce = Food(Vector2(792, 576), Color(117, 208, 72))
ketchup = Food(Vector2(1145, 489), Color(223, 164, 94))
mustard = Food(Vector2(1085, 494), Color(213, 151, 88))

# DRINKS

cup = Food(Vector2(300, 639), Color(113, 197, 239))
water = Food(Vector2(290, 459), Color(189, 222, 219))
orange_juice = Food(Vector2(256, 493), Color(195, 167, 101))
cherry_juice = Food(Vector2(353, 472), Color(172, 134, 149))
lime_juice = Food(Vector2(321, 493), Color(133, 204, 128))

# ICE CREAMS

cone = Food(Vector2(866, 562), Color(202, 143, 50))
white_scoop = Food(Vector2(916, 584), Color(255, 236, 192))
brown_scoop = Food(Vector2(976, 557), Color(197, 152, 114))
pink_scoop = Food(Vector2(1008, 611), Color(250, 205, 117))

AllFood = [
    chips, tomato, cheese, salad, sausage, lettuce,
    cup, water, orange_juice, cherry_juice,
    lime_juice, cone, white_scoop, ketchup,
    brown_scoop, pink_scoop, mustard
]

OrderZones = [
    OrderZone(Vector2(280, 100), Vector2(550, 220)),
    OrderZone(Vector2(570, 100), Vector2(840, 220)),
    OrderZone(Vector2(860, 100), Vector2(1130, 220))
]


def check_order_zones():
    for zone in OrderZones:
        for food in AllFood:
            if zone.check_for_color(food.unique_color):
                food.throw_food(zone.get_middle())


input("Нажмите ENTER, чтобы начать")

while True:
    check_order_zones()
    time.sleep(5000)