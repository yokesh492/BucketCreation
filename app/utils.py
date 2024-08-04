from PIL import Image
from io import BytesIO

def compress_image(file, quality=85):
    image = Image.open(file.file)
    image_format = image.format
    buffered = BytesIO()
    image.save(buffered, format=image_format, quality=quality)
    return buffered
