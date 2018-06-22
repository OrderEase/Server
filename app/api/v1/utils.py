from PIL import Image
from io import BytesIO
import base64
import re

def getImageFromBase64(dataURI):
    image_data = re.sub('^data:image/.+;base64,', '', dataURI)
    image = Image.open(BytesIO(base64.b64decode(image_data)))
    return image