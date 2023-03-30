import gc

import torch
from PIL import Image
import numpy as np
from RealESRGAN import RealESRGAN
import gc


def super_res(img_path):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    model = RealESRGAN(device, scale=4)
    model.load_weights('weights/RealESRGAN_x4.pth', download=True)
    image = Image.open(img_path).convert('RGB')

    sr_image = model.predict(image)
    path = 'sr_image.png'
    sr_image.save(path)
    gc.collect()
    torch.cuda.empty_cache()
    return sr_image, path
