import xml.etree.ElementTree as ET
from os import getcwd

sets=[('annotation_train', 'train'), ('annotation_val', 'val'), ('annotation_test0305', 'test0305')]

classes = ["bird"]


def convert_annotation( image_id, list_file):
    in_file = open('dataset/%s/%s.xml'%(anno_set, image_id), encoding="utf-8")
    tree=ET.parse(in_file)
    root = tree.getroot()

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        print(cls, type(cls))
        if cls == "capacitor3":
            cls_id = 0
            xmlbox = obj.find('bndbox')
            b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
            list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        print(cls_id, type(cls))
        xmlbox = obj.find('bndbox')
        b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
        list_file.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))

wd = getcwd()

for anno_set, image_set in sets:
    image_ids = open('dataset/%s/%s.txt'%(image_set, image_set)).read().strip().split()
    print(image_ids)
    list_file = open('%s.txt'%(anno_set), 'w')
    for image_id in image_ids:
        list_file.write('%s/dataset/%s/%s.jpg'%(wd,image_set, image_id))
        convert_annotation(image_id, list_file)
        list_file.write('\n')
    list_file.close()

