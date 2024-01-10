import matplotlib.pyplot as plt
from models import Point, LineSegment, Arc
import numpy as np
import math

def plot_path_with_markers(path, commands):
    fig, ax = plt.subplots()

    # Plot the original path
    for segment in path:
        if isinstance(segment, LineSegment):
            ax.plot([segment.start.x, segment.end.x], [segment.start.y, segment.end.y], 'b-')
        elif isinstance(segment, Arc):
            theta = np.linspace(math.radians(segment.start_angle), math.radians(segment.end_angle), 100)
            x = segment.center.x + segment.radius * np.cos(theta)
            y = segment.center.y + segment.radius * np.sin(theta)
            ax.plot(x, y, 'b-')

    # Simulate the cutting head movement based on commands
    head_position = [0, 0]
    for cmd in commands:
        if "X" in cmd:
            dx = float(cmd.split()[-1])
            head_position[0] += dx
        elif "Y" in cmd:
            dy = float(cmd.split()[-1])
            head_position[1] += dy
        # ax.plot(head_position[0], head_position[1], 'ro', markersize=10)

    plt.show()