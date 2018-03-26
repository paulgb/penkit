from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(name='penkit-optimize',
      version='0.0.2',
      description='Experimental SVG optimizer using or-tools.',
      long_description=readme(),
      author='Paul Butler',
      author_email='penkit@paulbutler.org',
      url='https://github.com/paulgb/penkit/optimizer',
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
