from PIL import Image
import base64
first_image = Image.open(r'D:\pythonProject8\train\static\image_data\{}'.format('2.jpg'))
img_resized = first_image.resize((129, 129), resample=Image.LANCZOS)
from io import BytesIO
img_bytes = BytesIO()
img_resized.save(img_bytes, format='JPEG')
img_binary = img_bytes.getvalue()
# print('img_binary',type(img_binary))
tital = base64.b64encode(img_binary).decode('utf-8')