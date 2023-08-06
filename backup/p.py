from PIL import Image
from PIL.ExifTags import TAGS
import sys

hi=Image.open(sys.argv[1])

[print(TAGS.get(k,k),v) for k,v in hi.getexif().items()]

hi.save(sys.argv[1].replace("jpg","png"),exif=hi.getexif())
