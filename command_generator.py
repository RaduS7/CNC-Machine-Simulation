import math
from models import Point, LineSegment, Arc

def generate_commands(path):
    commands = []
    current_position = Point(0, 0)

    for segment in path:
        if isinstance(segment, LineSegment):
            dx = segment.end.x - current_position.x
            dy = segment.end.y - current_position.y

            if dx != 0:
                commands.append(f"MOVE X {dx}")
            if dy != 0:
                commands.append(f"MOVE Y {dy}")

            current_position = segment.end

        elif isinstance(segment, Arc):
            steps = 10
            for i in range(1, steps + 1):
                angle = math.radians(segment.start_angle + i * (segment.end_angle - segment.start_angle) / steps)
                x = segment.center.x + segment.radius * math.cos(angle)
                y = segment.center.y + segment.radius * math.sin(angle)

                dx = x - current_position.x
                dy = y - current_position.y

                if dx != 0:
                    commands.append(f"MOVE X {dx}")
                if dy != 0:
                    commands.append(f"MOVE Y {dy}")

                current_position = Point(x, y)

    return commands