from buttons import buttons_dict
import config


import mouse_controller
import time

from PIL import ImageGrab, Image


class Color:
    def __init__(self, r: int, g: int, b: int):
        self.r = r
        self.g = g
        self.b = b

    def __str__(self):
        return f"{self.r} {self.g} {self.b}"

    def __eq__(self, other):
        return self.r == other.r and self.g == other.g and self.b == other.b


class Vector2:
    def __init__(self, x, y, need_convert: bool = True):
        if need_convert:
            x *= config.screen_resolution_x / 1280
            y *= config.screen_resolution_y / 768
        self.x = round(x)
        self.y = round(y)

    def __str__(self):
        return f"{self.x} {self.y}"


class Plate:
    coords: Vector2

    def __init__(self, coords: Vector2):
        self.coords = coords

    def throw(self, coords):
        mouse_controller.click(self.coords.x, self.coords.y)
        #  time.sleep(config.time_between_clicks)
        mouse_controller.click(coords.x, coords.y)


class Food:

    coords: Vector2
    unique_color: Color

    def __init__(self, coords: Vector2, unique_color: Color):
        self.coords = coords
        self.unique_color = unique_color

    def throw(self, coords):

        mouse_controller.click(self.coords.x, self.coords.y)
        time.sleep(config.time_between_clicks)
        mouse_controller.click(coords.x, coords.y)


class OrderZone:
    start: Vector2
    end: Vector2
    customer: Vector2

    def __init__(self, start: Vector2, end: Vector2, customer: Vector2):
        self.start = start
        self.end = end
        self.customer = customer

    def check_for_color(self, screen: Image, color: Color) -> bool:
        for x in range(int(self.start.x), int(self.end.x)):
            for y in range(int(self.start.y), int(self.end.y)):
                r, g, b = screen.getpixel((x, y))
                pixel_color = Color(r, g, b)

                if pixel_color == color:
                    return True

        return False


class Button:
    coords: Vector2
    unique_color: Color

    def __init__(self, coords: Vector2, unique_color: Color):
        self.coords = coords
        self.unique_color = unique_color

    def try_click(self, screen: Image):
        r, g, b = screen.getpixel((self.coords.x, self.coords.y))

        color = Color(r, g, b)

        if color == self.unique_color:
            print("Click")
            time.sleep(0.2)
            mouse_controller.click(self.coords.x, self.coords.y)
            time.sleep(0.2)


plate = Plate(Vector2(417, 553))

# FOOD
dish = Food(Vector2(1117, 650), Color(165, 181, 222))

bread = Food(Vector2(527, 500), Color(151, 97, 42))
chips = Food(Vector2(787, 509), Color(255, 105, 26))
tomato = Food(Vector2(705, 557), Color(201, 8, 8))
cheese = Food(Vector2(617, 557), Color(253, 215, 100))
salad = Food(Vector2(649, 484), Color(169, 182, 214))
sausage = Food(Vector2(530, 580), Color(244, 199, 189))
lettuce = Food(Vector2(792, 576), Color(125, 114, 34))
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
pink_scoop = Food(Vector2(1008, 611), Color(250, 205, 217))

# BUTTONS

text_screen_resolution = f"{config.screen_resolution_x}x{config.screen_resolution_y}"

Buttons = buttons_dict.get(text_screen_resolution)

if Buttons is None:
    config.click_buttons = False


# level_up_button = Button(Vector2(702, 601, False), Color(252, 253, 251))

# level_up_button2 = Button(Vector2(1144, 167, False), Color(121, 90, 134))




AllFood = [
    dish, bread, chips, tomato, cheese, salad, sausage, lettuce,
    cup, water, orange_juice, cherry_juice,
    lime_juice, cone, white_scoop, ketchup,
    brown_scoop, pink_scoop, mustard
]

OrderZones = [
    OrderZone(Vector2(280, 90), Vector2(550, 220), Vector2(423, 427)),
    OrderZone(Vector2(570, 90), Vector2(840, 220), Vector2(685, 402)),
    OrderZone(Vector2(860, 90), Vector2(1130, 220), Vector2(927, 415))
]


def try_to_click_buttons(screen):
    for button in Buttons:
        button.try_click(screen)


def check_order_zones(screen: Image):
    for zone in OrderZones:
        for food in AllFood:
            if zone.check_for_color(screen, food.unique_color):
                plate.throw(zone.customer)
                food.throw(zone.customer)


input("Нажмите ENTER, чтобы начать")

while True:
    screen = ImageGrab.grab().convert("RGB")
    if config.click_buttons:
        try_to_click_buttons(screen)
    check_order_zones(screen)
    time.sleep(config.time_between_iterations)
