from django import template
from os.path import basename, splitext

register = template.Library()

@register.filter(name='filename')
def filename(value):
    # Split the filename and extension
    filename, extension = splitext(basename(value))
    # Return the filename without the extension
    return filename
