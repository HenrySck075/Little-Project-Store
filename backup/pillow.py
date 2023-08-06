from PIL import Image, ImageFilter
import sys
image = Image.open(sys.argv[1]) 
def blur(box):
    crop_img = image.crop(box) 
    # Use GaussianBlur directly to blur the image 10 times. 
    blur_image = crop_img.filter(ImageFilter.GaussianBlur(radius=10)) 
    image.paste(blur_image, box) 

blur((0,1580,1080,2340))
image.save('a.jpg')
