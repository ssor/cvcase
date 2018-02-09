class CirclePara(object):
    def __init__(self, center, radius, color=None):
        self.center = center
        self.radius = radius
        if color is None:
            self.color = (0, 0, 255)
        else:
            self.color = color
