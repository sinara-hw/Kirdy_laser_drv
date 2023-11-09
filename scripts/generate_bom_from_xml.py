# Modified from "bom_csv_grouped_by_value_with_fp.py" Example BOM Generation Script

"""
    @package
    Output: CSV (comma-separated)
    The BOM does not include components with DNP or excluded from BOM field(s) checked. 
    Grouped By: Value, Footprint, MFR_PN, MFR_ALT
    Sorted By: Ref
    Fields: Ref, Value, MFR_PN, MFR_PN_ALT, Qnty, LibPart, Footprint

    Command line:
    python "pathToFile/generate_bom_from_xml.py" "%I" "%O.csv"
"""

import kicad_netlist_reader
import csv
import sys
import os

try:
    if not os.path.isdir(os.path.dirname(sys.argv[2])):
        os.makedirs(os.path.dirname(sys.argv[2]))
    f = open(sys.argv[2], 'w', encoding='utf-8')
except IOError:
    raise IOError("Can't open output file for writing: " + sys.argv[2])

# Custom Equal Operator for "groupComponents" method
def __eq__(self, other):
    result = False
    if self.getValue() == other.getValue():
        if self.getFootprint() == other.getFootprint():
            if self.getField("MFR_PN") == other.getField("MFR_PN"):
                if self.getField("MFR_PN_ALT") == other.getField("MFR_PN_ALT"):
                    result = True
    return result
kicad_netlist_reader.comp.__eq__ = __eq__

net = kicad_netlist_reader.netlist(sys.argv[1])

out = csv.writer(f, lineterminator='\n', delimiter=',', quotechar='\"', quoting=csv.QUOTE_ALL)
out.writerow(['Source:', net.getSource()])
out.writerow(['Date:', net.getDate()])
out.writerow(['Tool:', net.getTool()])
out.writerow(['Ref', 'Value', 'MFR_PN', 'MFR_PN_ALT', 'Qnty', 'LibPart', 'Footprint'])

grouped = net.groupComponents(components=net.getInterestingComponents(excludeBOM=True, DNP=True))

for group in grouped:
    refs = ""
    for component in group:
        if refs != "":
            refs += ", "
        refs += component.getRef()
        c = component

    out.writerow([refs,
        c.getValue(),
        c.getField("MFR_PN"),
        c.getField("MFR_PN_ALT"),
        len(group),
        c.getLibName() + ":" + c.getPartName(),
        c.getFootprint()])
