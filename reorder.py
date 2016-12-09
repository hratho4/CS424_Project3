import json
import xmltodict
from collections import OrderedDict as OD

# A script for converting the Illustrator-generated SVG into one which could be used with D3.  Probably disposable, and certainly not well documented, but maybe it can help somebody.

json_file   = open("index.json", 'r')
svg_in      = open("index.svg",  'r')
svg_out     = open("static/map.svg", 'w')

col_dict_from_json = json.loads(json_file.read())
neworder = sorted(col_dict_from_json.keys())
neworder.reverse()

root = xmltodict.parse(svg_in.read())

g_boxes_layer = root['svg']['g']['g']['g']

row_groups = list(range(32, 47))
row_groups.reverse()
rows = ['a', 'b', 'c']
rows.reverse()

col_groups = ['R5E', 'R6E', 'R7E', 'R8E', 'R9E', 'R10E', 'R11E', 'R12E', 'R13E', 'R14E', 'R15E', 'R16E', 'R17E']

# assign correct IDs to elements
for i, g1 in enumerate(g_boxes_layer['g']):
    i = len(g_boxes_layer['g']) - i - 1
    rowgroup_number = '{num:02d}'.format(num=row_groups[i])
    g1['@id'] = '{}'.format(rowgroup_number)
    for j, g2 in enumerate(g1['g']):
        row_letter = rows[j]
        g2['@id'] = '{}{}'.format(rowgroup_number, row_letter.upper())

        c = 0
        for l, polygon in enumerate(g2['polygon']):
            offset = len(g2['polygon']) - l - 1
            try:
                polygon['@id'] = col_dict_from_json[str(rowgroup_number)][row_letter][offset]
            except IndexError as err:
                m = len(col_dict_from_json[str(rowgroup_number)][row_letter])
                print('Missing in {}{}, json count: {}, offset: {}'.format(rowgroup_number, row_letter, len(col_dict_from_json[str(rowgroup_number)][row_letter]), offset))

svg_out.write(xmltodict.unparse(root, pretty=True))