import cv2
from PIL import Image

top_y_adjustment = 1.3
bottom_y_adjustment = 1.1
offset = 30

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

def blurCB_01(path):
    # Extract EXIF data from the original image using Pillow
    original_pil = Image.open(path)
    exif_data = original_pil.info.get('exif')
    
    # Load the image using OpenCV
    image = cv2.imread(path)
    kernel_size = (31, 31)  # Increase the kernel size for more blur

    # Define the coordinates for the first top left corner box
    top_left_x1 = int(image.shape[1] * 0.00)
    top_left_y1 = int(image.shape[0] * 0.115)
    bottom_left_x2 = int(image.shape[1] * 0.32)
    bottom_left_y2 = int(image.shape[0] * 0.41)
    blurred_roi_left1 = cv2.GaussianBlur(
        image[top_left_y1:bottom_left_y2, top_left_x1:bottom_left_x2],
        kernel_size, 0
    )

    # Define the coordinates for the second top left corner box
    top_left2_x1 = int(image.shape[1] * 0.32)
    top_left2_y1 = int(image.shape[0] * 0.115)
    bottom_left2_x2 = int(image.shape[1] * 0.40)
    bottom_left2_y2 = int(image.shape[0] * 0.41)
    blurred_roi_left2 = cv2.GaussianBlur(
        image[top_left2_y1:bottom_left2_y2, top_left2_x1:bottom_left2_x2],
        kernel_size, 0
    )

    # Define the coordinates for the third top left box
    top_left3_x1 = int(image.shape[1] * 0.40)
    top_left3_y1 = int(image.shape[0] * 0.20)
    bottom_left3_x2 = int(image.shape[1] * 0.48)
    bottom_left3_y2 = int(image.shape[0] * 0.38)
    blurred_roi_left3 = cv2.GaussianBlur(
        image[top_left3_y1:bottom_left3_y2, top_left3_x1:bottom_left3_x2],
        kernel_size, 0
    )

    # Define the coordinates for the right-middle box
    top_rmid_x1 = int(image.shape[1] * 0.68)
    top_rmid_y1 = int(image.shape[0] * 0.30)
    bottom_rmid_x2 = int(image.shape[1] * 1)
    bottom_rmid_y2 = int(image.shape[0] * 0.41)
    blurred_roi_rmid = cv2.GaussianBlur(
        image[top_rmid_y1:bottom_rmid_y2, top_rmid_x1:bottom_rmid_x2],
        kernel_size, 0
    )

    # Define the coordinates for the second right-middle box
    top_rmid2_x1 = int(image.shape[1] * 0.635)
    top_rmid2_y1 = int(image.shape[0] * 0.32)
    bottom_rmid2_x2 = int(image.shape[1] * 0.68)
    bottom_rmid2_y2 = int(image.shape[0] * 0.40)
    blurred_roi_rmid2 = cv2.GaussianBlur(
        image[top_rmid2_y1:bottom_rmid2_y2, top_rmid2_x1:bottom_rmid2_x2],
        kernel_size, 0
    )

    # Create a copy of the original image and update the regions with the blurred ROIs
    output = image.copy()
    output[top_left_y1:bottom_left_y2, top_left_x1:bottom_left_x2] = blurred_roi_left1
    output[top_left2_y1:bottom_left2_y2, top_left2_x1:bottom_left2_x2] = blurred_roi_left2
    output[top_left3_y1:bottom_left3_y2, top_left3_x1:bottom_left3_x2] = blurred_roi_left3
    output[top_rmid_y1:bottom_rmid_y2, top_rmid_x1:bottom_rmid_x2] = blurred_roi_rmid
    output[top_rmid2_y1:bottom_rmid2_y2, top_rmid2_x1:bottom_rmid2_x2] = blurred_roi_rmid2

    # Save the output image with the original EXIF data
    save_image_with_exif(path, output, exif_data)
    return 

def blurCB_01B(path):
    original_pil = Image.open(path)
    exif_data = original_pil.info.get('exif')
    
    image = cv2.imread(path)
    kernel_size = (31, 31)
    
    # Top left corner box
    top_left_x1 = int(image.shape[1] * 0.00)
    top_left_y1 = int(image.shape[0] * 0.16)
    bottom_left_x2 = int(image.shape[1] * 0.175)
    bottom_left_y2 = int(image.shape[0] * 0.51)
    blurred_roi_left1 = cv2.GaussianBlur(
        image[top_left_y1:bottom_left_y2, top_left_x1:bottom_left_x2],
        kernel_size, 0
    )
    
    # Middle box
    top_mid_x1 = int(image.shape[1] * 0.47)
    top_mid_y1 = int(image.shape[0] * 0.25)
    bottom_mid_x2 = int(image.shape[1] * 0.76)
    bottom_mid_y2 = int(image.shape[0] * 0.365)
    blurred_roi_mid = cv2.GaussianBlur(
        image[top_mid_y1:bottom_mid_y2, top_mid_x1:bottom_mid_x2],
        kernel_size, 0
    )
    
    # Second middle box
    top_mid2_x1 = int(image.shape[1] * 0.345)
    top_mid2_y1 = int(image.shape[0] * 0.25)
    bottom_mid2_x2 = int(image.shape[1] * 0.47)
    bottom_mid2_y2 = int(image.shape[0] * 0.37)
    blurred_roi_mid2 = cv2.GaussianBlur(
        image[top_mid2_y1:bottom_mid2_y2, top_mid2_x1:bottom_mid2_x2],
        kernel_size, 0
    )
    
    # Top right box
    top_rmid_x1 = int(image.shape[1] * 0.76)
    top_rmid_y1 = int(image.shape[0] * 0.175)
    bottom_rmid_x2 = int(image.shape[1] * 1)
    bottom_rmid_y2 = int(image.shape[0] * 0.39)
    blurred_roi_rmid = cv2.GaussianBlur(
        image[top_rmid_y1:bottom_rmid_y2, top_rmid_x1:bottom_rmid_x2],
        kernel_size, 0
    )
    
    output = image.copy()
    output[top_left_y1:bottom_left_y2, top_left_x1:bottom_left_x2] = blurred_roi_left1
    output[top_mid_y1:bottom_mid_y2, top_mid_x1:bottom_mid_x2] = blurred_roi_mid
    output[top_mid2_y1:bottom_mid2_y2, top_mid2_x1:bottom_mid2_x2] = blurred_roi_mid2
    output[top_rmid_y1:bottom_rmid_y2, top_rmid_x1:bottom_rmid_x2] = blurred_roi_rmid
    
    save_image_with_exif(path, output, exif_data)
    return 

def blurCB_02(path):
    original_pil = Image.open(path)
    exif_data = original_pil.info.get('exif')
    
    image = cv2.imread(path)
    kernel_size = (31, 31)
    
    # Top left corner box
    top_left_x1 = int(image.shape[1] * 0.00)
    top_left_y1 = int(image.shape[0] * 0.00)
    bottom_left_x2 = int(image.shape[1] * 0.11)
    bottom_left_y2 = int(image.shape[0] * 0.405)
    blurred_roi_left1 = cv2.GaussianBlur(
        image[top_left_y1:bottom_left_y2, top_left_x1:bottom_left_x2],
        kernel_size, 0
    )
    
    # Middle box
    top_mid_x1 = int(image.shape[1] * 0.65)
    top_mid_y1 = int(image.shape[0] * 0.06)
    bottom_mid_x2 = int(image.shape[1] * 0.73)
    bottom_mid_y2 = int(image.shape[0] * 0.29)
    blurred_roi_mid = cv2.GaussianBlur(
        image[top_mid_y1:bottom_mid_y2, top_mid_x1:bottom_mid_x2],
        kernel_size, 0
    )
    
    # Second middle box
    top_mid2_x1 = int(image.shape[1] * 0.535)
    top_mid2_y1 = int(image.shape[0] * 0.06)
    bottom_mid2_x2 = int(image.shape[1] * 0.65)
    bottom_mid2_y2 = int(image.shape[0] * 0.25)
    blurred_roi_mid2 = cv2.GaussianBlur(
        image[top_mid2_y1:bottom_mid2_y2, top_mid2_x1:bottom_mid2_x2],
        kernel_size, 0
    )
    
    # Third middle box
    top_mid3_x1 = int(image.shape[1] * 0.19)
    top_mid3_y1 = int(image.shape[0] * 0.125)
    bottom_mid3_x2 = int(image.shape[1] * 0.42)
    bottom_mid3_y2 = int(image.shape[0] * 0.28)
    blurred_roi_mid3 = cv2.GaussianBlur(
        image[top_mid3_y1:bottom_mid3_y2, top_mid3_x1:bottom_mid3_x2],
        kernel_size, 0
    )
    
    # Top right box
    top_rmid_x1 = int(image.shape[1] * 0.78)
    top_rmid_y1 = int(image.shape[0] * 0.02)
    bottom_rmid_x2 = int(image.shape[1] * 1)
    bottom_rmid_y2 = int(image.shape[0] * 0.36)
    blurred_roi_rmid = cv2.GaussianBlur(
        image[top_rmid_y1:bottom_rmid_y2, top_rmid_x1:bottom_rmid_x2],
        kernel_size, 0
    )
    
    # Second top right box
    top_rmid2_x1 = int(image.shape[1] * 0.73)
    top_rmid2_y1 = int(image.shape[0] * 0.10)
    bottom_rmid2_x2 = int(image.shape[1] * 0.78)
    bottom_rmid2_y2 = int(image.shape[0] * 0.31)
    blurred_roi_rmid2 = cv2.GaussianBlur(
        image[top_rmid2_y1:bottom_rmid2_y2, top_rmid2_x1:bottom_rmid2_x2],
        kernel_size, 0
    )
    
    output = image.copy()
    output[top_left_y1:bottom_left_y2, top_left_x1:bottom_left_x2] = blurred_roi_left1
    output[top_mid_y1:bottom_mid_y2, top_mid_x1:bottom_mid_x2] = blurred_roi_mid
    output[top_mid2_y1:bottom_mid2_y2, top_mid2_x1:bottom_mid2_x2] = blurred_roi_mid2
    output[top_mid3_y1:bottom_mid3_y2, top_mid3_x1:bottom_mid3_x2] = blurred_roi_mid3
    output[top_rmid_y1:bottom_rmid_y2, top_rmid_x1:bottom_rmid_x2] = blurred_roi_rmid
    output[top_rmid2_y1:bottom_rmid2_y2, top_rmid2_x1:bottom_rmid2_x2] = blurred_roi_rmid2
    
    save_image_with_exif(path, output, exif_data)
    return 

def blurCB_03(path):
    original_pil = Image.open(path)
    exif_data = original_pil.info.get('exif')
    
    image = cv2.imread(path)
    kernel_size = (31, 31)
    
    # First top left corner box
    top_left_x1 = int(image.shape[1] * 0.00)
    top_left_y1 = int(image.shape[0] * 0.09)
    bottom_left_x2 = int(image.shape[1] * 0.35)
    bottom_left_y2 = int(image.shape[0] * 0.26)
    blurred_roi_left1 = cv2.GaussianBlur(
        image[top_left_y1:bottom_left_y2, top_left_x1:bottom_left_x2],
        kernel_size, 0
    )
    
    # Second top left corner box
    top_left2_x1 = int(image.shape[1] * 0.35)
    top_left2_y1 = int(image.shape[0] * 0.09)
    bottom_left2_x2 = int(image.shape[1] * 0.60)
    bottom_left2_y2 = int(image.shape[0] * 0.22)
    blurred_roi_left2 = cv2.GaussianBlur(
        image[top_left2_y1:bottom_left2_y2, top_left2_x1:bottom_left2_x2],
        kernel_size, 0
    )
    
    # Top middle box
    top_mid_x1 = int(image.shape[1] * 0.60)
    top_mid_y1 = int(image.shape[0] * 0.09)
    bottom_mid_x2 = int(image.shape[1] * 0.76)
    bottom_mid_y2 = int(image.shape[0] * 0.19)
    blurred_roi_mid = cv2.GaussianBlur(
        image[top_mid_y1:bottom_mid_y2, top_mid_x1:bottom_mid_x2],
        kernel_size, 0
    )
    
    output = image.copy()
    output[top_left_y1:bottom_left_y2, top_left_x1:bottom_left_x2] = blurred_roi_left1
    output[top_left2_y1:bottom_left2_y2, top_left2_x1:bottom_left2_x2] = blurred_roi_left2
    output[top_mid_y1:bottom_mid_y2, top_mid_x1:bottom_mid_x2] = blurred_roi_mid
    
    save_image_with_exif(path, output, exif_data)
    return 

def blurDE_01(path):
    original_pil = Image.open(path)
    exif_data = original_pil.info.get('exif')
    
    image = cv2.imread(path)
    kernel_size = (75, 75)
    
    # Second left-middle box
    top2_left_x = int(image.shape[1] * 0.15)
    top2_left_y = int(image.shape[0] * 0.57)
    bottom2_right_x = int(image.shape[1] * 0.30)
    bottom2_right_y = int(image.shape[0] * 1)
    
    # Left-middle box
    top_left_x = int(image.shape[1] * 0.00)
    top_left_y = int(image.shape[0] * 0.50)
    bottom_right_x = int(image.shape[1] * 0.15)
    bottom_right_y = int(image.shape[0] * 1)
    
    # Third left-middle box
    top3_left_x = int(image.shape[1] * 0.30)
    top3_left_y = int(image.shape[0] * 0.70)
    bottom3_right_x = int(image.shape[1] * 0.60)
    bottom3_right_y = int(image.shape[0] * 1)
    
    # Fourth left-middle box
    top4_left_x = int(image.shape[1] * 0.60)
    top4_left_y = int(image.shape[0] * 0.77)
    bottom4_right_x = int(image.shape[1] * 0.95)
    bottom4_right_y = int(image.shape[0] * 1)
    
    blurred_roi_left = cv2.GaussianBlur(
        image[top_left_y:bottom_right_y, top_left_x:bottom_right_x],
        kernel_size, 0
    )
    blurred_roi_left2 = cv2.GaussianBlur(
        image[top2_left_y:bottom2_right_y, top2_left_x:bottom2_right_x],
        kernel_size, 0
    )
    blurred_roi_left3 = cv2.GaussianBlur(
        image[top3_left_y:bottom3_right_y, top3_left_x:bottom3_right_x],
        kernel_size, 0
    )
    blurred_roi_left4 = cv2.GaussianBlur(
        image[top4_left_y:bottom4_right_y, top4_left_x:bottom4_right_x],
        kernel_size, 0
    )
    
    output = image.copy()
    output[top_left_y:bottom_right_y, top_left_x:bottom_right_x] = blurred_roi_left
    output[top2_left_y:bottom2_right_y, top2_left_x:bottom2_right_x] = blurred_roi_left2
    output[top3_left_y:bottom3_right_y, top3_left_x:bottom3_right_x] = blurred_roi_left3
    output[top4_left_y:bottom4_right_y, top4_left_x:bottom4_right_x] = blurred_roi_left4
    
    save_image_with_exif(path, output, exif_data)
    return 

def blurDE_03(path):
    original_pil = Image.open(path)
    exif_data = original_pil.info.get('exif')
    
    image = cv2.imread(path)
    kernel_size = (31, 31)
    
    # Top left corner region
    top_left_x = int(image.shape[1] * 0.00)
    top_left_y = int(image.shape[0] * 0.45)
    bottom_right_x = int(image.shape[1] * 0.08)
    bottom_right_y = int(image.shape[0] * 0.52)
    blurred_roi_left = cv2.GaussianBlur(
        image[top_left_y:bottom_right_y, top_left_x:bottom_right_x],
        kernel_size, 0
    )
    
    # Middle left region
    top_left2_x = int(image.shape[1] * 0.08)
    top_left2_y = int(image.shape[0] * 0.45)
    bottom_right2_x = int(image.shape[1] * 0.24)
    bottom_right2_y = int(image.shape[0] * 0.52)
    blurred_roi_left_middle = cv2.GaussianBlur(
        image[top_left2_y:bottom_right2_y, top_left2_x:bottom_right2_x],
        kernel_size, 0
    )
    
    # Top middle region
    top_mid1_x = int(image.shape[1] * 0.10)
    top_mid1_y = int(image.shape[0] * 0.33)
    bottom_mid1_x = int(image.shape[1] * 0.57)
    bottom_mid1_y = int(image.shape[0] * 0.40)
    blurred_roi_top_middle = cv2.GaussianBlur(
        image[top_mid1_y:bottom_mid1_y, top_mid1_x:bottom_mid1_x],
        kernel_size, 0
    )
    
    # Top right corner
    top_right3_x = int(image.shape[1] * 0.80)
    top_right3_y = int(image.shape[0] * 0.35)
    bottom_right3_x = int(image.shape[1] * 1)
    bottom_right3_y = int(image.shape[0] * 0.44)
    blurred_roi_top_right = cv2.GaussianBlur(
        image[top_right3_y:bottom_right3_y, top_right3_x:bottom_right3_x],
        kernel_size, 0
    )
    
    # Middle right region
    top_right_mid_x = int(image.shape[1] * 0.82)
    top_right_mid_y = int(image.shape[0] * 0.485)
    bottom_right_mid_x = int(image.shape[1] * 1)
    bottom_right_mid_y = int(image.shape[0] * 1)
    blurred_roi_middle_right = cv2.GaussianBlur(
        image[top_right_mid_y:bottom_right_mid_y, top_right_mid_x:bottom_right_mid_x],
        kernel_size, 0
    )
    
    output = image.copy()
    output[top_left_y:bottom_right_y, top_left_x:bottom_right_x] = blurred_roi_left
    output[top_left2_y:bottom_right2_y, top_left2_x:bottom_right2_x] = blurred_roi_left_middle
    output[top_mid1_y:bottom_mid1_y, top_mid1_x:bottom_mid1_x] = blurred_roi_top_middle
    output[top_right3_y:bottom_right3_y, top_right3_x:bottom_right3_x] = blurred_roi_top_right
    output[top_right_mid_y:bottom_right_mid_y, top_right_mid_x:bottom_right_mid_x] = blurred_roi_middle_right
    
    save_image_with_exif(path, output, exif_data)
    return 

def blurNB_01(path):
    original_pil = Image.open(path)
    exif_data = original_pil.info.get('exif')
    
    image = cv2.imread(path)
    kernel_size = (71, 71)
    
    # Top left corner region
    top_left_x = int(image.shape[1] * 0.00)
    top_left_y = int(image.shape[0] * 0.32)
    bottom_right_x = int(image.shape[1] * 0.13)
    bottom_right_y = int(image.shape[0] * 0.40)
    blurred_roi_left = cv2.GaussianBlur(
        image[top_left_y:bottom_right_y, top_left_x:bottom_right_x],
        kernel_size, 0
    )
    
    output = image.copy()
    output[top_left_y:bottom_right_y, top_left_x:bottom_right_x] = blurred_roi_left
    
    save_image_with_exif(path, output, exif_data)
    return 

def blurNB_02(path):
    original_pil = Image.open(path)
    exif_data = original_pil.info.get('exif')
    
    image = cv2.imread(path)
    kernel_size = (31, 31)
    
    # Top middle region
    top_mid1_x = int(image.shape[1] * 0)
    top_mid1_y = int(image.shape[0] * 0.26)
    bottom_mid1_x = int(image.shape[1] * 0.35)
    bottom_mid1_y = int(image.shape[0] * 0.38)
    blurred_roi_top_middle = cv2.GaussianBlur(
        image[top_mid1_y:bottom_mid1_y, top_mid1_x:bottom_mid1_x],
        kernel_size, 0
    )
    
    # Top right region
    top_right3_x = int(image.shape[1] * 0.58)
    top_right3_y = int(image.shape[0] * 0.24)
    bottom_right3_x = int(image.shape[1] * 1)
    bottom_right3_y = int(image.shape[0] * 0.315)
    blurred_roi_top_right = cv2.GaussianBlur(
        image[top_right3_y:bottom_right3_y, top_right3_x:bottom_right3_x],
        kernel_size, 0
    )
    
    output = image.copy()
    output[top_mid1_y:bottom_mid1_y, top_mid1_x:bottom_mid1_x] = blurred_roi_top_middle
    output[top_right3_y:bottom_right3_y, top_right3_x:bottom_right3_x] = blurred_roi_top_right
    
    save_image_with_exif(path, output, exif_data)
    return 

def blurBF_01(path):
    original_pil = Image.open(path)
    exif_data = original_pil.info.get('exif')
    
    image = cv2.imread(path)
    kernel_size = (71, 71)
    
    # First middle region
    top_middle_x1 = int(image.shape[1] * 0.00)
    top_middle_y1 = int(image.shape[0] * 0.00)
    bottom_middle_x2 = int(image.shape[1] * 0.65)
    bottom_middle_y2 = int(image.shape[0] * 0.20)
    blurred_roi_middle = cv2.GaussianBlur(
        image[top_middle_y1:bottom_middle_y2, top_middle_x1:bottom_middle_x2],
        kernel_size, 0
    )
    
    # Second middle region
    top_middle2_x1 = int(image.shape[1] * 0.65)
    top_middle2_y1 = int(image.shape[0] * 0.00)
    bottom_middle2_x2 = int(image.shape[1] * 1)
    bottom_middle2_y2 = int(image.shape[0] * 0.24)
    blurred_roi_middle2 = cv2.GaussianBlur(
        image[top_middle2_y1:bottom_middle2_y2, top_middle2_x1:bottom_middle2_x2],
        kernel_size, 0
    )
    
    output = image.copy()
    # The order of updating regions can be maintained as needed
    output[top_middle2_y1:bottom_middle2_y2, top_middle2_x1:bottom_middle2_x2] = blurred_roi_middle2
    output[top_middle_y1:bottom_middle_y2, top_middle_x1:bottom_middle_x2] = blurred_roi_middle
    
    save_image_with_exif(path, output, exif_data)
    return 

def blur_image(camera_ID, path):
    match camera_ID:
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
        case 'BF_01':
            blurBF_01(path)
        case _:
            return
