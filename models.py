class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class LineSegment:
    def __init__(self, start: Point, end: Point):
        self.start = start
        self.end = end

class Arc:
    def __init__(self, center: Point, radius, start_angle, end_angle):
        self.center = center
        self.radius = radius
        self.start_angle = start_angle
        self.end_angle = end_angle