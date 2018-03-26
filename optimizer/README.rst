
Generate optimized SVG with default options (~5 minute runtime):

    penkit-optimize input.svg output.svg

Don't optimize anything, just visualize the transits:

    penkit-optimize input.svg --visualize vis.svg

Run greedy optimization, save the file, and save a visualization of the result.

    penkit-optimize input.svg output.svg --greedy --visualize vis.svg

Run the full optimization and write a visualization of the result:

    penkit-optimize input.svg output.svg --visualize vis.svg
