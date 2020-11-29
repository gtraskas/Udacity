import xml.etree.cElementTree as ET

# '.iterparse()' not only iterates through (and parses) each element of a xml file,
# but it also builds the complete 'tree' in memory.
# There are very few computers that can hold a 2GB file in memory.
# The following get_element() function stops the '.iterparse()' method from building the complete tree in memory.
# Instead, once it has finished processing an element, it removes each element from memory with 'root.clear()' method.
# Essentially it creates a generator, yield (which in this code is each of the individual elements of the osm file).
# The important part is that the values for 'yield' are not stored in memory, they are generated in each iteration.

def get_element(osm_file): 
    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end':
            yield elem
            root.clear()

