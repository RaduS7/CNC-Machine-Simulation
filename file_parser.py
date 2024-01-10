def read_path_from_file(filename):
    from models import Point, LineSegment, Arc
    
    path = []
    with open(filename, 'r') as file:
        for line in file:
            if line.strip():
                tokens = line.strip().split()
                if tokens[0] == "LINE":
                    start = Point(float(tokens[1]), float(tokens[2]))
                    end = Point(float(tokens[3]), float(tokens[4]))
                    path.append(LineSegment(start, end))
                elif tokens[0] == "ARC":
                    center = Point(float(tokens[1]), float(tokens[2]))
                    radius = float(tokens[3])
                    start_angle = float(tokens[4])
                    end_angle = float(tokens[5])
                    path.append(Arc(center, radius, start_angle, end_angle))
    return path