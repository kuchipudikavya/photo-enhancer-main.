import schemas as _schemas
import os
from PIL import Image
from io import BytesIO
import uuid
import numpy as np
import base64
from enhancer.enhancer import Enhancer


TEMP_PATH = 'temp'
ENHANCE_METHOD = os.getenv('METHOD', 'gfpgan')  # Simplified default assignment
BACKGROUND_ENHANCEMENT = os.getenv('BACKGROUND_ENHANCEMENT', 'True')  # Default as string
BACKGROUND_ENHANCEMENT = BACKGROUND_ENHANCEMENT.lower() == 'true'  # Convert to boolean

enhancer = Enhancer(
    method=ENHANCE_METHOD, 
    background_enhancement=BACKGROUND_ENHANCEMENT, 
    upscale=2
)


async def enhance(enhanceBase: _schemas._EnhanceBase) -> str:
    # Decode the base64 image
    image_data = base64.b64decode(enhanceBase.encoded_base_img[0])
    
    # Open the image and convert to numpy array
    with Image.open(BytesIO(image_data)) as img:
        init_image = np.array(img)
    
    # Enhance the image
    restored_image = enhancer.enhance(init_image)
    
    # Convert back to PIL Image and encode as base64
    final_image = Image.fromarray(restored_image)
    buffered = BytesIO()
    final_image.save(buffered, format="JPEG")
    encoded_img = base64.b64encode(buffered.getvalue()).decode('utf-8')  # Decode bytes to string
    
    return encoded_img