from colour import Color

def get_color(color):

    return [x * 255.0 for x in Color(color).rgb]