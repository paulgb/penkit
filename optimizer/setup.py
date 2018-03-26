from setuptools import setup

setup(name='penkit-optimize',
      version='0.0.1',
      description='Experimental SVG optimizer using or-tools.',
      author='Paul Butler',
      author_email='penkit@paulbutler.org',
      url='https://github.com/paulgb/penkit',
      packages=['penkit_optimize'],
      entry_points={
          'console_scripts': [
              'penkit-optimize = penkit_optimize.cli:main'
          ]
      },
      install_requires=[
          'ortools>=6.7.4973',
          'Rtree>=0.8.3',
          'svgpathtools>=1.3.2',
      ])
