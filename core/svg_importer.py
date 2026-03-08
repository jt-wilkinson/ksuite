from svgpathtools import svg2paths
from core.object_model import VectorObject


def import_svg(filepath):

    paths, attributes = svg2paths(filepath)

    objects = []

    for path in paths:

        obj = VectorObject(path)
        objects.append(obj)

    return objects