import xml.etree.ElementTree as ET
import json

def export_xml():
    data = ET.Element('parent')
    sub_data = ET.SubElement(data, 'child')
    sub_sub_data = ET.SubElement(sub_data, 'child-of-child')

    data.text = "ROOT"
    sub_data.text = "CHILD"
    sub_sub_data.text = "CHILD-of-CHILD"

    data_file = ET.tostring(data)

    with open("testing-data.xml", "wb") as file:
        file.write(data_file)

export_xml()

family = {
    "child1" : {
        "name" : "Suck",
        "year" : 6969
    },
    "child2" : {
        "name" : "My",
        "year" : 4200
    },
    "child3" : {
        "name" : "Balls",
        "year" : 2077
    }
}

print(family["child1"]["name"])
print(family["child2"]["year"])

# Load a JSON file
file = open('object-data.json')
profile = json.load(file)

print(profile["bruh"][1])
print(profile["layer1"])
print(profile["layer1"]["layer2"])
print(profile["layer1"]["layer2"]["layer3"])

file.close()

# Write a JSON file
file = open("output.json", "w")
json.dump(family, file)