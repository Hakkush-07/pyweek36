WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
GRAY = (150, 150, 150)
LIGHT_BLUE = (150, 150, 255)
SPACE = (20, 20, 80)
STAR = (255, 255, 100)

def hsv2rgb(h, s, v):
    mx = 255 * v
    mn = mx * (1 - s)
    z = (mx - mn) * (1 - abs((h / 60) % 2 - 1))
    r = mn if 120 <= h < 240 else mx if h < 60 or h >= 300 else z + mn
    g = mn if 240 <= h else mx if 60 <= h < 180 else z + mn
    b = mn if h < 120 else mx if 180 <= h < 300 else z + mn
    return round(r), round(g), round(b)
