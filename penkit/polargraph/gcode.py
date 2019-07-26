from math import sqrt
import re
import numpy as np
import svgpathtools


try:
    import matplotlib.pyplot as plt
except ImportError:
    pass

class PolargraphGCode:
    def __init__(self, height=3000, width=7000, speed=1200, max_speed=7000):
        self.height = height
        self.width = width
        self.diagonal = sqrt((self.width/2)**2 + self.height**2)
        self.max_speed = max_speed
        self.speed = speed

    def cartesian_to_polargraph(self, x, y):
        a = sqrt(x ** 2 + y ** 2) - self.diagonal
        b = sqrt((self.width-x) ** 2 + y ** 2) - self.diagonal
        
        return a, b

    def svg_to_polargraph(self, svg_file):
        lines, _ = svgpathtools.svg2paths(svg_file)

        last = None
        for line in lines:
            a_start, b_start = self.cartesian_to_polargraph(line.start.real, line.start.imag)
            if line.start != last:
                yield 0, a_start, b_start, self.max_speed
            
            a, b = self.cartesian_to_polargraph(line.end.real, line.end.imag)
            
            proj_dist = sqrt((a_start-a)**2 + (b_start-b)**2)
            orig_dist = abs(line.end - line.start)
            if orig_dist > 0:
                speed = int(self.speed * (proj_dist / orig_dist))
                
                yield 1, a, b, speed

                last = line.end
        
        yield 0, 0.0, 0.0, self.max_speed
    
    def polargraph_time(self, commands):
        time = 0
        last_x = 0
        last_y = 0
        for _, x, y, speed in commands:
            dist = sqrt((x-last_x)**2 + (y-last_y)**2)
            time += dist / speed
            last_y = y
            last_x = x
        return time

    def polargraph_to_gcode(self, commands):
            yield from [
                    'M999',
                    'M204 S500',
                    'G90',
                    'G92 X0 Y0',
                    'M72 P2',
                    'M71 (Marker Change)',
                    'G4 S1.00',
                    'M106',
                    'G4 P100',
                ]
            
            for i, a, b, speed in commands:
                yield f'G{i} X{a:.3f} Y{b:.3f} F{speed}'

    def polargraph_to_cartesian(self, a, b):
        a += self.diagonal
        b += self.diagonal
        x = (a ** 2 - b ** 2 + self.width ** 2) / (2 * self.width)
        try:
            y = self.height - sqrt(a ** 2 - x ** 2)
        except ValueError:
            y = self.height
        return x, y

    def read_gcode_file(self, filename):
        with open(filename) as gcfile:
            for line in gcfile:
                match = re.match('G([01]) X(-?\d+\.\d+) Y(-?\d+\.\d+) F(.+)', line)
                if match:
                    i, a, b, f = (float(f) for f in match.groups())
                    x, y = self.polargraph_to_cartesian(a, b)
                    yield i, x, y, f

    def plot_gcode_file(self, filename):
        parts = self.read_gcode_file(filename)
        x_hard = list()
        x_soft = list()
        y_hard = list()
        y_soft = list()

        x_loc = self.width / 2
        y_loc = 0
        for i, x, y, f in parts:
            if i == 0:
                x_hard.append(np.nan)
                y_hard.append(np.nan)
                x_soft.extend([np.nan, x_loc, x])
                y_soft.extend([np.nan, y_loc, y])

            x_hard.append(x)
            y_hard.append(y)

            x_loc = x
            y_loc = y

        plt.plot(x_hard, y_hard, c='blue')
        plt.plot(x_soft, y_soft, c='#dddddd')
        axis = plt.gca()
        axis.set_aspect('equal')
        
