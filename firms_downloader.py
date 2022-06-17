import xml.dom.minidom
import urllib
import io

from xml.dom.minidom import parse

FIRMS_URL = ""
LOWER_LAT = 45.693156241109214
UPPER_LAT = 52.44345069237891
LOWER_LON = 22.43180504054893
UPPER_LON = 40.62348468945702


def is_coordinate_in_bounds(raw_coordinate):
    coordinate = str(raw_coordinate).replace(" ", "")
    coordinates = coordinate.split(",")
    lon = float(coordinates[0])
    lat = float(coordinates[1])

    if lat > LOWER_LAT and lat < UPPER_LAT and lon > LOWER_LON and lon < UPPER_LON:
        print (coordinate + " in ukraine")
        return True

    print (coordinate + " not in ukraine")
    return False

def main():
    # Open XML document using minidom parser
    with xml.dom.minidom.parse("MODIS_C6_1_Europe_24h.kml") as dom:

        coordinates = dom.documentElement.getElementsByTagName("coordinates")

        to_remove = []
        count = 0
        for coordinate in coordinates:
            coordinate_value = coordinate.firstChild.nodeValue
            in_bounds = is_coordinate_in_bounds(coordinate_value)
            count = count + 1
            if not in_bounds:
                to_remove.append(coordinate.parentNode.parentNode)

        folder = dom.documentElement.getElementsByTagName("Folder")[0]
        for remove_node in to_remove:
            folder.removeChild (remove_node)

        with open("output.kml", "w") as f:
            f.write(dom.saveXML(dom.documentElement))

main()