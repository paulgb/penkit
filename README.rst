Penkit
======

**Penkit** is a library of utility functions generating `pen plots <https://en.wikipedia.org/wiki/Plotter>`__ from Python/numpy.

Installation
------------

Requirements: Python 2.7 or 3.x, `numpy`, `scipy`. Preview modules require `ipython` or `matplotlib`.

    # pip install penkit

Documentation
-------------

- Download the `tutorial notebooks <tutorial>`_ or `run them on Binder <https://mybinder.org/v2/gh/paulgb/penkit.git/master?filepath=tutorial>`_
- `Module Documentation <http://penkit.readthedocs.io/en/latest/>`_

Examples
--------

Grid Surface Projection
~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from penkit.textures import make_grid_texture
    from penkit.textures.util import rotate_texture
    from penkit.surfaces import make_noise_surface
    from penkit.write import write_plot
    from penkit.projection import project_and_occlude_texture
    
    # create a texture
    grid_density = 68
    texture = make_grid_texture(grid_density, grid_density, 100)
    
    # rotate the texture
    texture = rotate_texture(texture, rotation=65)
    
    # create the surface
    surface = make_noise_surface(blur=28, seed=12345) * 10
    
    # project the texture onto the surface
    proj = project_and_occlude_texture(texture, surface, angle=69)
    
    # plot the result
    write_plot([proj], 'examples/grid_surface.svg')

.. image:: examples/grid_surface.svg
   :width: 400px

Hilbert Curve Surface Projection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from penkit.fractal import hilbert_curve
    from penkit.textures.util import fit_texture, rotate_texture
    from penkit.surfaces import make_noise_surface
    from penkit.projection import project_and_occlude_texture
    from penkit.write import write_plot
    
    # create a texture
    texture = hilbert_curve(7)
    
    # rotate the texture
    texture = rotate_texture(texture, 30)
    texture = fit_texture(texture)
    
    # create the surface
    surface = make_noise_surface(blur=30) * 5
    
    # project the texture onto the surface
    proj = project_and_occlude_texture(texture, surface, 50)
    
    # plot the result
    write_plot([proj], 'examples/hilbert_surface.svg')

.. image:: examples/hilbert_surface.svg
   :width: 400px

----

.. image:: https://travis-ci.org/paulgb/penkit.svg?branch=master
   :target: https://travis-ci.org/paulgb/penkit

.. image:: https://mybinder.org/badge.svg
   :target: https://mybinder.org/v2/gh/paulgb/penkit.git/master?filepath=tutorial
