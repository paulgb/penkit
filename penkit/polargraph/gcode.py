from math import sqrt
import re
import numpy as np
import svgpathtools


try:
    import matplotlib.pyplot as plt
except ImportError:
    pass

class PolargraphGCode:
    def __init__(self, height=7000, width=3000, speed=1200, max_speed=7000):
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
            speed = int(self.speed * (proj_dist / orig_dist))
            
            yield 1, a, b, speed

            last = line.end
        
        yield 0, 0.0, 0.0, self.max_speed
    
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
                yield f'G{i} X{a:.3f} Y{b:.3f} {speed}'

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
        parts = list(self.read_gcode_file(filename))
        i, x, y, f = zip(*parts)

        i = np.array(i)
        x_hard = x_soft = np.array(x)
        y_hard = y_soft = np.array(y)

        x_hard[i == 0] = y_hard[i == 0] = np.nan
        x_soft[i == 1] = y_soft[i == 1] = np.nan

        plt.plot(x_hard, y_hard, c='blue')
        plt.plot(x_soft, y_soft, c='#dddddd')
        axis = plt.gca()
        axis.set_aspect('equal')
        
