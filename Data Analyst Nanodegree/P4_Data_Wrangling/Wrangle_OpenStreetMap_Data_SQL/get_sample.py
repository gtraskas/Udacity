import iterative_parsing as ip
import xml.etree.cElementTree as ET

OSM_FILE = "san-jose_california.osm"
SAMPLE_FILE = "sample.osm"

k = 10 # Parameter: take every k-th top level element
    
with open(SAMPLE_FILE, 'wb') as output:
    output.write(bytes('<?xml version="1.0" encoding="UTF-8"?>\n', 'UTF-8'))
    output.write(bytes('<osm>\n  ', 'UTF-8'))

    # Write every 10th top level element
    for i, element in enumerate(ip.get_element(OSM_FILE)):
        if i % 10 == 0:
            output.write(ET.tostring(element, encoding='utf-8'))

    output.write(bytes('</osm>', 'UTF-8'))

