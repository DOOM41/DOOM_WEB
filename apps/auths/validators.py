from rest_framework.exceptions import ValidationError
import xml.etree.cElementTree as et


def is_svg(filename):
    tag = None
    with open(filename, "r") as f:
        try:
            for event, el in et.iterparse(f, ('start',)):
                tag = el.tag
                break
        except et.ParseError:
            pass
    return tag == '{http://www.w3.org/2000/svg}svg'

def validate_svg(file, valid):
    if not is_svg(file):
        raise ValidationError("File not svg")
