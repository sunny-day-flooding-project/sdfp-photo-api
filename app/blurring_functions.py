import cv2
import json
import numpy as np
from PIL import Image

def save_image_with_exif(path, output, exif_data):
    """
    Convert the OpenCV (BGR) image to a PIL Image (RGB) and save it.
    If exif_data is provided, include the EXIF metadata in the saved image.
    """
    # OpenCV uses BGR format, so convert to RGB
    rgb_output = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(rgb_output)
    if exif_data:
        pil_img.save(path, exif=exif_data)
    else:
        pil_img.save(path)
        
def blur_regions(image, polygons, kernel_size=(21,21), sigma_x=10):
    
    height, width = image.shape[:2]
    mask = np.zeros((height, width), dtype=np.uint8)
    
    for polygon in polygons['shapes']:
        if polygon['shape_type'] != 'polygon':
            continue
    
        points = np.array(polygon['points'], dtype=np.int32)
        cv2.fillPoly(mask, [points], color=255)
    
    # --- Blur entire image ---
    blurred = cv2.GaussianBlur(image, kernel_size, sigmaX=sigma_x)

    # --- Composite blurred regions using the mask ---
    mask_3ch = cv2.merge([mask] * 3)  # Make 3-channel mask
    output = np.where(mask_3ch == 255, blurred, image)
    
    return output

def blurBF_01(path):
    # Extract EXIF data from the original image using Pillow
    original_pil = Image.open(path)
    exif_data = original_pil.info.get('exif')
    
    # Load the image using OpenCV
    image = cv2.imread(path)
    polygons = json.load(open('app/camera_blur_regions/BF_01_blur.json'))

    output = blur_regions(image, polygons)

    # Save the output image with the original EXIF data
    save_image_with_exif(path, output, exif_data)
    return 

def blurCB_01(path):
    # Extract EXIF data from the original image using Pillow
    original_pil = Image.open(path)
    exif_data = original_pil.info.get('exif')
    
    # Load the image using OpenCV
    image = cv2.imread(path)
    polygons = json.load(open('app/camera_blur_regions/CB_01_blur.json'))

    output = blur_regions(image, polygons)

    # Save the output image with the original EXIF data
    save_image_with_exif(path, output, exif_data)
    return 

def blurCB_01B(path):
    # Extract EXIF data from the original image using Pillow
    original_pil = Image.open(path)
    exif_data = original_pil.info.get('exif')
    
    # Load the image using OpenCV
    image = cv2.imread(path)
    polygons = json.load(open('app/camera_blur_regions/CB_01B_blur.json'))

    output = blur_regions(image, polygons)

    # Save the output image with the original EXIF data
    save_image_with_exif(path, output, exif_data)
    return 

def blurCB_02(path):
    # Extract EXIF data from the original image using Pillow
    original_pil = Image.open(path)
    exif_data = original_pil.info.get('exif')
    
    # Load the image using OpenCV
    image = cv2.imread(path)
    polygons = json.load(open('/code/app/camera_blur_regions/CB_02_blur.json'))

    output = blur_regions(image, polygons)

    # Save the output image with the original EXIF data
    save_image_with_exif(path, output, exif_data)
    return 

def blurCB_03(path):
    # Extract EXIF data from the original image using Pillow
    original_pil = Image.open(path)
    exif_data = original_pil.info.get('exif')
    
    # Load the image using OpenCV
    image = cv2.imread(path)
    polygons = json.load(open('app/camera_blur_regions/CB_03_blur.json'))

    output = blur_regions(image, polygons)

    # Save the output image with the original EXIF data
    save_image_with_exif(path, output, exif_data)
    return 

def blurDE_01(path):
    # Extract EXIF data from the original image using Pillow
    original_pil = Image.open(path)
    exif_data = original_pil.info.get('exif')
    
    # Load the image using OpenCV
    image = cv2.imread(path)
    polygons = json.load(open('app/camera_blur_regions/DE_01_blur.json'))

    output = blur_regions(image, polygons)

    # Save the output image with the original EXIF data
    save_image_with_exif(path, output, exif_data)
    return 

def blurDE_03(path):
    # Extract EXIF data from the original image using Pillow
    original_pil = Image.open(path)
    exif_data = original_pil.info.get('exif')
    
    # Load the image using OpenCV
    image = cv2.imread(path)
    polygons = json.load(open('app/camera_blur_regions/DE_03_blur.json'))

    output = blur_regions(image, polygons)

    # Save the output image with the original EXIF data
    save_image_with_exif(path, output, exif_data)
    return 

def blurNB_01(path):
    # Extract EXIF data from the original image using Pillow
    original_pil = Image.open(path)
    exif_data = original_pil.info.get('exif')
    
    # Load the image using OpenCV
    image = cv2.imread(path)
    polygons = json.load(open('app/camera_blur_regions/NB_01_blur.json'))

    output = blur_regions(image, polygons)

    # Save the output image with the original EXIF data
    save_image_with_exif(path, output, exif_data)
    return 

def blurNB_02(path):
    # Extract EXIF data from the original image using Pillow
    original_pil = Image.open(path)
    exif_data = original_pil.info.get('exif')
    
    # Load the image using OpenCV
    image = cv2.imread(path)
    polygons = json.load(open('app/camera_blur_regions/NB_02_blur.json'))

    output = blur_regions(image, polygons)

    # Save the output image with the original EXIF data
    save_image_with_exif(path, output, exif_data)
    return

def blurNR_01(path):
    # Extract EXIF data from the original image using Pillow
    original_pil = Image.open(path)
    exif_data = original_pil.info.get('exif')
    
    # Load the image using OpenCV
    image = cv2.imread(path)
    polygons = json.load(open('app/camera_blur_regions/NR_01_blur.json'))

    output = blur_regions(image, polygons)

    # Save the output image with the original EXIF data
    save_image_with_exif(path, output, exif_data)
    return  

def blur_image(camera_ID, path):
    match camera_ID:
        case 'BF_01':
            blurBF_01(path)
        case 'CB_01':
            blurCB_01(path)
        case 'CB_01B':
            blurCB_01B(path)
        case 'CB_02':
            blurCB_02(path)
        case 'CB_03':
            blurCB_03(path)
        case 'DE_01':
            blurDE_01(path)
        case 'DE_03':
            blurDE_03(path)
        case 'NB_01':
            blurNB_01(path)
        case 'NB_02':
            blurNB_02(path)
        case 'NR_01':
            blurNR_01(path)
        case _:
            return
