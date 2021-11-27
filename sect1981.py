# SECTOR 1981
# Old-school Traveller subsector generator.
# Using Strict 1981 3-Booklet Classic Traveller rules.
# By Omer Golan-Joel, golan2072@gmail.com

import worldgen
import agama
import hexmap

if __name__ == '__main__':
    with open("output.txt", 'w') as output:
        subsector_worlds = worldgen.generate_subsector()
        output.write(worldgen.string_subsector(subsector_worlds))
        starmap = hexmap.generate_starmap(subsector_worlds)
        output.write(hexmap.starmap_string(starmap))