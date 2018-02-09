class LinePara(object):
    def __init__(self, start, end, color=None, thickness=None):
        self.start = start
        self.end = end
        if color is None:
            self.color = (0, 0, 255)
        else:
            self.color = color
        if thickness is None:
            self.thickness = 2
        else:
            self.thickness = thickness

    def to_json(self):
        return {
            "start": self.start.to_json(),
            "end": self.end.to_json(),
        }
