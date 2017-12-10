import matplotlib.pyplot as plt

def draw_layer(ax, layer):
    ax.set_aspect('equal', 'datalim')
    ax.plot(*layer)
    ax.axis('off')


def draw_plot(ax, plot):
    for layer in plot:
        show_layer(ax, layer)
    

def show_layer(layer):
    fig, ax = plt.subplots()
    draw_layer(ax, layer)


def show_plot(plot):
    fig, ax = plt.subplots()
    draw_plot(ax, plot)
