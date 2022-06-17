import xml.dom.minidom
import urllib.request
import os

from xml.dom.minidom import parse

KML_SOURCE_DIRECTORY = ".\\"
KML_OUTPUT_FILE_PREFIX = "filtered"
DOWNLOAD_FROM_FIRMS = True

BOUNDS_LABEL = "Ukraine"
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
        print("{0} in {1}".format(coordinate, BOUNDS_LABEL))
        return True

    print("{0} not in {1}".format(coordinate, BOUNDS_LABEL))
    return False


def filter_coordinates(input_path):
    # Open XML document using minidom parser
    file_name = os.path.basename(input_path)
    output_file_name = "{0}_{1}".format(KML_OUTPUT_FILE_PREFIX, file_name)

    print("Processing {0} to {1}".format(file_name, output_file_name))

    with xml.dom.minidom.parse(input_path) as dom:
        coordinates = dom.documentElement.getElementsByTagName("coordinates")

        to_remove = []
        for coordinate in coordinates:
            coordinate_value = coordinate.firstChild.nodeValue
            in_bounds = is_coordinate_in_bounds(coordinate_value)
            if not in_bounds:
                to_remove.append(coordinate.parentNode.parentNode)

        folder = dom.documentElement.getElementsByTagName("Folder")[0]
        for remove_node in to_remove:
            folder.removeChild(remove_node)

        with open(output_file_name, "w") as f:
            f.write(dom.saveXML(dom.documentElement))


def get_input_files(source_file_directory):
    directories = os.listdir(source_file_directory)
    input_files = []
    for file in directories:
        file_name = os.path.basename(file)
        file_ext = os.path.splitext(file)[1]
        if file_ext == ".kml" and not KML_OUTPUT_FILE_PREFIX in file_name:
            input_files.append(file)

    return input_files


def download_file(url, output_path):
    print('Downloading {0} to {1}'.format(url, output_path))
    urllib.request.urlretrieve(url, output_path)


def main():

    if DOWNLOAD_FROM_FIRMS == True:
        urls = ["https://firms.modaps.eosdis.nasa.gov/data/active_fire/modis-c6.1/kml/MODIS_C6_1_Europe_24h.kml",
                "https://firms.modaps.eosdis.nasa.gov/data/active_fire/suomi-npp-viirs-c2/kml/SUOMI_VIIRS_C2_Europe_24h.kml",
                "https://firms.modaps.eosdis.nasa.gov/data/active_fire/noaa-20-viirs-c2/kml/J1_VIIRS_C2_Europe_24h.kml",
                "https://firms.modaps.eosdis.nasa.gov/data/active_fire/modis-c6.1/kml/MODIS_C6_1_Russia_Asia_24h.kml",
                "https://firms.modaps.eosdis.nasa.gov/data/active_fire/suomi-npp-viirs-c2/kml/SUOMI_VIIRS_C2_Russia_Asia_24h.kml",
                "https://firms.modaps.eosdis.nasa.gov/data/active_fire/noaa-20-viirs-c2/kml/J1_VIIRS_C2_Russia_Asia_24h.kml"
                ]

        print('Downloading KML files')
        for url in urls:
            parts = url.split('/')
            output_path = KML_SOURCE_DIRECTORY + parts[len(parts) - 1]
            download_file(url, output_path)

    print('Getting input KML for processing')
    input_files = get_input_files(KML_SOURCE_DIRECTORY)

    if len(input_files) > 0:
        print('Processing KML files')
        for input_file in input_files:
            filter_coordinates(input_file)
    else:
        print("No KML files to process")

    print('Done')


main()
