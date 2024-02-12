import cv2
from PIL import Image

top_y_adjustment = 1.3
bottom_y_adjustment = 1.1
offset = 30

def blurCB_01(path):
    # Load the image 
    image = cv2.imread(path) ## Access image here- input image to be blurred 

    kernel_size = (31, 31)  # Increase the kernel size for more blur

    # Define the coordinates for the first top left corner box
    # Top coordinates
    top_left_x1 = int(image.shape[1] * .00)  # Adjust the fraction as needed
    top_left_y1 = int(image.shape[0] * .10 + offset)  

    #Bottom coordinates
    bottom_left_x2 = int(image.shape[1] * .32)
    bottom_left_y2 = int(image.shape[0] * .44 + offset)  # Adjust the fraction as needed

    # Blur the region of interest (top left corner box 1)
    blurred_roi_left1 = cv2.GaussianBlur(image[top_left_y1:bottom_left_y2, top_left_x1:bottom_left_x2], kernel_size, 0)

    # Define the coordinates for the second top left corner box
    # Top coordinates
    top_left2_x1 = int(image.shape[1] * .32)  # Adjust the fraction as needed
    top_left2_y1 = int(image.shape[0] * .10 + offset)  

    #Bottom coordinates
    bottom_left2_x2 = int(image.shape[1] * .40)
    bottom_left2_y2 = int(image.shape[0] * .44 + offset)  # Adjust the fraction as needed

    # Blur the region of interest (top left corner box 2)
    blurred_roi_left2 = cv2.GaussianBlur(image[top_left2_y1:bottom_left2_y2, top_left2_x1:bottom_left2_x2], kernel_size, 0)

    #Define the coordinates for the third top left box
    # Top coordinates 
    top_left3_x1 = int(image.shape[1] * .40) 
    top_left3_y1 = int(image.shape[0] * .20 + offset) 

    # Bottom coordinates

    bottom_left3_x2 = int(image.shape[1] * .495)
    bottom_left3_y2 = int(image.shape[0] * .40 + offset)

    # Blur the region of interest (top left corner box 2)
    blurred_roi_left3 = cv2.GaussianBlur(image[top_left3_y1:bottom_left3_y2, top_left3_x1:bottom_left3_x2], kernel_size, 0)

    # Define the coordinates for the right-middle box
    # Top coordinates
    top_rmid_x1 = int(image.shape[1] * .68)  # Adjust the fraction as needed
    top_rmid_y1 = int(image.shape[0] * .28 + offset) # Bottom adjustment seems to work better here

    #Bottom coordinates
    bottom_rmid_x2 = int(image.shape[1] * 1)
    bottom_rmid_y2 = int(image.shape[0] * .46 + offset)  # Adjust the fraction as needed

    # Blur the region of interest (right-middle box)
    blurred_roi_rmid = cv2.GaussianBlur(image[top_rmid_y1:bottom_rmid_y2, top_rmid_x1:bottom_rmid_x2], kernel_size, 0)


    # Define the coordinates for the second right-middle box
    # Top coordinates
    top_rmid2_x1 = int(image.shape[1] * .62)  # Adjust the fraction as needed
    top_rmid2_y1 = int(image.shape[0] * .30 + offset) # Bottom adjustment seems to work better here 

    #Bottom coordinates
    bottom_rmid2_x2 = int(image.shape[1] * .68)
    bottom_rmid2_y2 = int(image.shape[0] * .42 + offset)  # Adjust the fraction as needed

    # Blur the region of interest (second right-middle box)
    blurred_roi_rmid2 = cv2.GaussianBlur(image[top_rmid2_y1:bottom_rmid2_y2, top_rmid2_x1:bottom_rmid2_x2], kernel_size, 0)

    # Create a copy of the original image
    output = image.copy()

    # Add the blurred region to the first section of the top left corner
    output[top_left_y1:bottom_left_y2, top_left_x1:bottom_left_x2] = blurred_roi_left1

    # Add the blurred region to the second section of the top left corner
    output[top_left2_y1:bottom_left2_y2, top_left2_x1:bottom_left2_x2] = blurred_roi_left2

    # Add the blurred region to the third section of the top left corner
    output[top_left3_y1:bottom_left3_y2, top_left3_x1:bottom_left3_x2] = blurred_roi_left3

    # Add the blurred region to the right-middle area
    output[top_rmid_y1:bottom_rmid_y2, top_rmid_x1:bottom_rmid_x2] = blurred_roi_rmid

    # Add the blurred region to the second right-middle area
    output[top_rmid2_y1:bottom_rmid2_y2, top_rmid2_x1:bottom_rmid2_x2] = blurred_roi_rmid2

    # Save the output image
    cv2.imwrite(path, output) # Can be modified to not output photo
    return 

def blurCB_01B(path):
    # Load the image 
    image = cv2.imread(path) ## Access image here- input image to be blurred 

    kernel_size = (31, 31)  # Increase the kernel size for more blur

    # Define the coordinates for the top left corner box
    # Top coordinates
    top_left_x1 = int(image.shape[1] * .00)  # Adjust the fraction as needed
    top_left_y1 = int(image.shape[0] * .16 + offset)  

    #Bottom coordinates
    bottom_left_x2 = int(image.shape[1] * .19)
    bottom_left_y2 = int(image.shape[0] * .51 + offset)  # Adjust the fraction as needed

    # Blur the region of interest (top left corner box)
    blurred_roi_left1 = cv2.GaussianBlur(image[top_left_y1:bottom_left_y2, top_left_x1:bottom_left_x2], kernel_size, 0)

    # Define the coordinates for the middle box
    # Top coordinates
    top_mid_x1 = int(image.shape[1] * .47)  # Adjust the fraction as needed
    top_mid_y1 = int(image.shape[0] * .19 + offset)  

    #Bottom coordinates
    bottom_mid_x2 = int(image.shape[1] * .76)
    bottom_mid_y2 = int(image.shape[0] * .33 + offset)  # Adjust the fraction as needed

    # Blur the region of interest (middle box)
    blurred_roi_mid = cv2.GaussianBlur(image[top_mid_y1:bottom_mid_y2, top_mid_x1:bottom_mid_x2], kernel_size, 0)

    # Define the coordinates for the second middle box
    # Top coordinates
    top_mid2_x1 = int(image.shape[1] * .31)  # Adjust the fraction as needed
    top_mid2_y1 = int(image.shape[0] * .19 + offset)  

    #Bottom coordinates
    bottom_mid2_x2 = int(image.shape[1] * .47)
    bottom_mid2_y2 = int(image.shape[0] * .32 + offset)  # Adjust the fraction as needed

    # Blur the region of interest (middle box)
    blurred_roi_mid2 = cv2.GaussianBlur(image[top_mid2_y1:bottom_mid2_y2, top_mid2_x1:bottom_mid2_x2], kernel_size, 0)

    # Define the coordinates for the top-right box
    # Top coordinates
    top_rmid_x1 = int(image.shape[1] * .76)  # Adjust the fraction as needed
    top_rmid_y1 = int(image.shape[0] * .10 + offset)  

    #Bottom coordinates
    bottom_rmid_x2 = int(image.shape[1] * 1)
    bottom_rmid_y2 = int(image.shape[0] * .35 + offset)  # Adjust the fraction as needed

    # Blur the region of interest (top right box)
    blurred_roi_rmid = cv2.GaussianBlur(image[top_rmid_y1:bottom_rmid_y2, top_rmid_x1:bottom_rmid_x2], kernel_size, 0)

    # Create a copy of the original image
    output = image.copy()

    # Add the blurred region to the top left corner
    output[top_left_y1:bottom_left_y2, top_left_x1:bottom_left_x2] = blurred_roi_left1

    # Add the blurred region to the middle section
    output[top_mid_y1:bottom_mid_y2, top_mid_x1:bottom_mid_x2] = blurred_roi_mid


    # Add the blurred region to the middle section
    output[top_mid2_y1:bottom_mid2_y2, top_mid2_x1:bottom_mid2_x2] = blurred_roi_mid2


    # Add the blurred region to the top right section
    output[top_rmid_y1:bottom_rmid_y2, top_rmid_x1:bottom_rmid_x2] = blurred_roi_rmid

    # Save the output image
    cv2.imwrite(path, output) # Can be modified to not output photo
    return 

def blurCB_02(path):
    # Load the image
    image = cv2.imread(path) ## Access image here 

    kernel_size = (31, 31)  # Increase the kernel size for more blur

    # Define the coordinates for the top left corner box
    # Top coordinates
    top_left_x1 = int(image.shape[1] * .00)  # Adjust the fraction as needed
    top_left_y1 = int(image.shape[0] * .06 * 1.4)  

    #Bottom coordinates
    bottom_left_x2 = int(image.shape[1] * .25)
    bottom_left_y2 = int(image.shape[0] * .245 * 1.3)  # Adjust the fraction as needed

    # Blur the region of interest (top left corner box)
    blurred_roi_left1 = cv2.GaussianBlur(image[top_left_y1:bottom_left_y2, top_left_x1:bottom_left_x2], kernel_size, 0)

    # Define the coordinates for the middle box
    # Top coordinates
    top_mid_x1 = int(image.shape[1] * .52)  # Adjust the fraction as needed
    top_mid_y1 = int(image.shape[0] * .03 * 1.6)  

    #Bottom coordinates
    bottom_mid_x2 = int(image.shape[1] * .675)
    bottom_mid_y2 = int(image.shape[0] * .29 * bottom_y_adjustment)  # Adjust the fraction as needed

    # Blur the region of interest (middle box) 
    blurred_roi_mid = cv2.GaussianBlur(image[top_mid_y1:bottom_mid_y2, top_mid_x1:bottom_mid_x2], kernel_size, 0)

    # Define the coordinates for the second top middle box
    # Top coordinates
    top_mid2_x1 = int(image.shape[1] * .45)  # Adjust the fraction as needed
    top_mid2_y1 = int(image.shape[0] * .03 * 1.5)  

    #Bottom coordinates
    bottom_mid2_x2 = int(image.shape[1] * .52)
    bottom_mid2_y2 = int(image.shape[0] * .26 * bottom_y_adjustment)  # Adjust the fraction as needed

    # Blur the region of interest  (second middle box) 
    blurred_roi_mid2 = cv2.GaussianBlur(image[top_mid2_y1:bottom_mid2_y2, top_mid2_x1:bottom_mid2_x2], kernel_size, 0)


    # Define the coordinates for the third top middle box
    # Top coordinates
    top_mid3_x1 = int(image.shape[1] * .36)  # Adjust the fraction as needed
    top_mid3_y1 = int(image.shape[0] * .1)  

    #Bottom coordinates
    bottom_mid3_x2 = int(image.shape[1] * .45)
    bottom_mid3_y2 = int(image.shape[0] * .215 * top_y_adjustment)  # Adjust the fraction as needed

    # Blur the region of interest  (third middle box) 
    blurred_roi_mid3 = cv2.GaussianBlur(image[top_mid3_y1:bottom_mid3_y2, top_mid3_x1:bottom_mid3_x2], kernel_size, 0)


    # Define the coordinates for the top right box
    # Top coordinates
    top_rmid_x1 = int(image.shape[1] * .675)  # Adjust the fraction as needed
    top_rmid_y1 = int(image.shape[0] * .05)  

    #Bottom coordinates
    bottom_rmid_x2 = int(image.shape[1] * 1)
    bottom_rmid_y2 = int(image.shape[0] * .355 * 1.2)  # Adjust the fraction as needed

    # Blur the region of interest (top right)
    blurred_roi_rmid = cv2.GaussianBlur(image[top_rmid_y1:bottom_rmid_y2, top_rmid_x1:bottom_rmid_x2], kernel_size, 0)


    # Define the coordinates for the second top right box
    # Top coordinates
    top_rmid2_x1 = int(image.shape[1] * .595)  # Adjust the fraction as needed
    top_rmid2_y1 = int(image.shape[0] * .29)  

    #Bottom coordinates
    bottom_rmid2_x2 = int(image.shape[1] * .675)
    bottom_rmid2_y2 = int(image.shape[0] * .35 * 1.1)  # Adjust the fraction as needed

    # Blur the region of interest (second top right box)
    blurred_roi_rmid2 = cv2.GaussianBlur(image[top_rmid2_y1:bottom_rmid2_y2, top_rmid2_x1:bottom_rmid2_x2], kernel_size, 0)


    # Create a copy of the original image
    output = image.copy()

    # Add the blurred region to the top left corner
    output[top_left_y1:bottom_left_y2, top_left_x1:bottom_left_x2] = blurred_roi_left1

    # Add the blurred region to the middle section
    output[top_mid_y1:bottom_mid_y2, top_mid_x1:bottom_mid_x2] = blurred_roi_mid

    # Add the blurred region to the second middle section
    output[top_mid2_y1:bottom_mid2_y2, top_mid2_x1:bottom_mid2_x2] = blurred_roi_mid2

    # Add the blurred region to the third middle section
    output[top_mid3_y1:bottom_mid3_y2, top_mid3_x1:bottom_mid3_x2] = blurred_roi_mid3

    # Add the blurred region to the top right section
    output[top_rmid_y1:bottom_rmid_y2, top_rmid_x1:bottom_rmid_x2] = blurred_roi_rmid

    # Add the blurred region to the second top right section
    output[top_rmid2_y1:bottom_rmid2_y2, top_rmid2_x1:bottom_rmid2_x2] = blurred_roi_rmid2

    # Save the output image
    cv2.imwrite(path, output) # Can be modified to not output photo
    return 

def blurCB_03(path):
    # Load the image
    image = cv2.imread(path) ## Access image here 

    kernel_size = (31, 31)  # Increase the kernel size for more blur

    # Define the coordinates for the first top left corner box
    # Top coordinates
    top_left_x1 = int(image.shape[1] * .00)  # Adjust the fraction as needed
    top_left_y1 = int(image.shape[0] * .09 * top_y_adjustment)  

    #Bottom coordinates
    bottom_left_x2 = int(image.shape[1] * .35)
    bottom_left_y2 = int(image.shape[0] * .30 * bottom_y_adjustment)  # Adjust the fraction as needed

    # Blur the region of interest (top left corner box 1)
    blurred_roi_left1 = cv2.GaussianBlur(image[top_left_y1:bottom_left_y2, top_left_x1:bottom_left_x2], kernel_size, 0)

    # Define the coordinates for the second top left corner box
    # Top coordinates
    top_left2_x1 = int(image.shape[1] * .35)  # Adjust the fraction as needed
    top_left2_y1 = int(image.shape[0] * .09 * top_y_adjustment)  

    #Bottom coordinates
    bottom_left2_x2 = int(image.shape[1] * .58)
    bottom_left2_y2 = int(image.shape[0] * .24 * bottom_y_adjustment)  # Adjust the fraction as needed

    # Blur the region of interest (top left corner box 2)
    blurred_roi_left2 = cv2.GaussianBlur(image[top_left2_y1:bottom_left2_y2, top_left2_x1:bottom_left2_x2], kernel_size, 0)

    # Define the coordinates for the top middle box
    # Top coordinates
    top_mid_x1 = int(image.shape[1] * .58)  # Adjust the fraction as needed
    top_mid_y1 = int(image.shape[0] * .09 * top_y_adjustment)  

    #Bottom coordinates
    bottom_mid_x2 = int(image.shape[1] * .77)
    bottom_mid_y2 = int(image.shape[0] * .18 * bottom_y_adjustment)  # Adjust the fraction as needed

    # Blur the region of interest (top middle)
    blurred_roi_mid = cv2.GaussianBlur(image[top_mid_y1:bottom_mid_y2, top_mid_x1:bottom_mid_x2], kernel_size, 0)

    # Create a copy of the original image
    output = image.copy()

    # Add the blurred region to the first section of the top left corner
    output[top_left_y1:bottom_left_y2, top_left_x1:bottom_left_x2] = blurred_roi_left1

    # Add the blurred region to the second section of the top left corner
    output[top_left2_y1:bottom_left2_y2, top_left2_x1:bottom_left2_x2] = blurred_roi_left2

    # Add the blurred region to the top middle 
    output[top_mid_y1:bottom_mid_y2, top_mid_x1:bottom_mid_x2] = blurred_roi_mid

    # Save the output image
    cv2.imwrite(path, output) # Can be modified to not output photo
    return 

def blurDE_01(path):
    # Load the image
    image = cv2.imread(path) ## Access image here 

    kernel_size = (31, 31)  # Increase the kernel size for more blur

    # Define the coordinates for the left-middle box 
    # Define the top coordinates
    top_left_x = int(image.shape[1] * .00)  # Adjust the fraction as needed
    top_left_y = int(image.shape[0] * .35)  # Adjust the fraction as needed

    # Define the bottom coordinates
    bottom_right_x = int(image.shape[1] * .30)
    bottom_right_y = int(image.shape[0] * .97)  # Adjust the fraction as needed

    # Define the coordinates for the second left-middle box 
    # Define the top coordinates
    top2_left_x = int(image.shape[1] * .30)  # Adjust the fraction as needed
    top2_left_y = int(image.shape[0] * .38)  # Adjust the fraction as needed

    # Define the bottom coordinates
    bottom2_right_x = int(image.shape[1] * .65)
    bottom2_right_y = int(image.shape[0] * .94)  # Adjust the fraction as needed

    # Blur the region of interest (middle-left box)
    blurred_roi_left = cv2.GaussianBlur(image[top_left_y:bottom_right_y, top_left_x:bottom_right_x], kernel_size, 0)

    # Blur the region of interest (Second middle-left box)
    blurred_roi_left2 = cv2.GaussianBlur(image[top2_left_y:bottom2_right_y, top2_left_x:bottom2_right_x], kernel_size, 0)


    # Create a copy of the original image
    output = image.copy()

    # Add the blurred region to the top left corner
    output[top_left_y:bottom_right_y, top_left_x:bottom_right_x] = blurred_roi_left

    # Add the second blurred region to the top left corner
    output[top2_left_y:bottom2_right_y, top2_left_x:bottom2_right_x] = blurred_roi_left2

    # Save the output image
    cv2.imwrite(path, output) # Can be modified to not output photo
    return 

def blurDE_03(path):
    # Load the image
    image = cv2.imread(path) ## Access image here 

    kernel_size = (31, 31)  # Increase the kernel size for more blur

    # Define the coordinates for the top left corner
    # Top coordinates
    top_left_x = int(image.shape[1] * .00)  # Adjust the fraction as needed
    top_left_y = int(image.shape[0] * .32 + offset)  # Adjust the fraction as needed

    # Bottom coordinates
    bottom_right_x = int(image.shape[1] * .08)
    bottom_right_y = int(image.shape[0] * .50 + offset)  # Adjust the fraction as needed

    # Blur the region of interest (top left corner)
    blurred_roi_left = cv2.GaussianBlur(image[top_left_y:bottom_right_y, top_left_x:bottom_right_x], kernel_size, 0)


    # Define the coordinates for the middle left region
    # Top coordinates
    top_left2_x = int(image.shape[1] * .08)  # Adjust the fraction as needed
    top_left2_y = int(image.shape[0] * .41 + offset)  # Adjust the fraction as needed

    # Bottom coordinates
    bottom_right2_x = int(image.shape[1] * .28)
    bottom_right2_y = int(image.shape[0] * .46 + offset)  # Adjust the fraction as needed

    # Blur the region of interest (middle left region)
    blurred_roi_left_middle = cv2.GaussianBlur(image[top_left2_y:bottom_right2_y, top_left2_x:bottom_right2_x], kernel_size, 0)


    # Define the coordinates for the middle top region
    # Top coordinates
    top_mid1_x = int(image.shape[1] * .12)  # Adjust the fraction as needed
    top_mid1_y = int(image.shape[0] * .27 + offset)  # Adjust the fraction as needed

    # Bottom coordinates
    bottom_mid1_x = int(image.shape[1] * .57)
    bottom_mid1_y = int(image.shape[0] * .37 + offset)  # Adjust the fraction as needed

    # Blur the region of interest (middle top region)
    blurred_roi_top_middle = cv2.GaussianBlur(image[top_mid1_y:bottom_mid1_y, top_mid1_x:bottom_mid1_x], kernel_size, 0)


    # Define the coordinates for the top right corner
    # Top coordinates
    top_right3_x = int(image.shape[1] * .73)  # Adjust the fraction as needed
    top_right3_y = int(image.shape[0] * .27 + offset)  # Adjust the fraction as needed

    # Bottom coordinates
    bottom_right3_x = int(image.shape[1] * 1)
    bottom_right3_y = int(image.shape[0] * .39 + offset) 

    # Blur the region of interest (top right corner)
    blurred_roi_top_right = cv2.GaussianBlur(image[top_right3_y:bottom_right3_y, top_right3_x:bottom_right3_x], kernel_size, 0)

    # Define the coordinates for the top right-middle section
    # Top coordinates
    top_right_mid_x = int(image.shape[1] * .78)  # Adjust the fraction as needed
    top_right_mid_y = int(image.shape[0] * .46 + offset)  # Adjust the fraction as needed


    # Bottom coordinates
    bottom_right_mid_x = int(image.shape[1] * 1)
    bottom_right_mid_y = int(image.shape[0] * 1 + offset) 

    # Blur the region of interest (right-middle section)
    blurred_roi_middle_right = cv2.GaussianBlur(image[top_right_mid_y:bottom_right_mid_y, top_right_mid_x:bottom_right_mid_x], kernel_size, 0)


    # Create a copy of the original image
    output = image.copy()

    # Add the blurred region to the mid left corner
    output[top_left_y:bottom_right_y, top_left_x:bottom_right_x] = blurred_roi_left

    # Add the blurred region adjacent to the mid left region
    output[top_left2_y:bottom_right2_y, top_left2_x:bottom_right2_x] = blurred_roi_left_middle 

    # Add the blurred region to the top middle region
    output[top_mid1_y:bottom_mid1_y, top_mid1_x:bottom_mid1_x] = blurred_roi_top_middle

    # Add the blurred region to the top right corner
    output[top_right3_y:bottom_right3_y, top_right3_x:bottom_right3_x] = blurred_roi_top_right

    # Add the blurred region to the middle-right region
    output[top_right_mid_y:bottom_right_mid_y, top_right_mid_x:bottom_right_mid_x] = blurred_roi_middle_right
    
    # Save the output image
    cv2.imwrite(path, output) # Can be modified to not output photo
    return 

def blurNB_02(path):
    # Load the image
    image = cv2.imread(path) ## Access image here 

    kernel_size = (31, 31)  # Increase the kernel size for more blur

    # Define the coordinates for the middle top region
    # Top coordinates
    top_mid1_x = int(image.shape[1] * 0)  # Adjust the fraction as needed
    top_mid1_y = int(image.shape[0] * .20 + offset)  # Adjust the fraction as needed

    # Bottom coordinates
    bottom_mid1_x = int(image.shape[1] * .52)
    bottom_mid1_y = int(image.shape[0] * .36 + offset)  # Adjust the fraction as needed

    # Blur the region of interest (top left corner)
    blurred_roi_top_middle = cv2.GaussianBlur(image[top_mid1_y:bottom_mid1_y, top_mid1_x:bottom_mid1_x], kernel_size, 0)


    # Define the coordinates for the top right corner
    # Top coordinates
    top_right3_x = int(image.shape[1] * .74)  # Adjust the fraction as needed
    top_right3_y = int(image.shape[0] * 0 + offset)  # Adjust the fraction as needed

    # Bottom coordinates
    bottom_right3_x = int(image.shape[1] * 1)
    bottom_right3_y = int(image.shape[0] * .32 + offset) 

    # Blur the region of interest (top right corner)
    blurred_roi_top_right = cv2.GaussianBlur(image[top_right3_y:bottom_right3_y, top_right3_x:bottom_right3_x], kernel_size, 0)

    # Define the coordinates for the second top right corner box
    # Top coordinates
    top_right_x = int(image.shape[1] * .59)  # Adjust the fraction as needed
    top_right_y = int(image.shape[0] * .20 + offset)  # Adjust the fraction as needed

    # Bottom coordinates
    bottom_right_x = int(image.shape[1] * .74)
    bottom_right_y = int(image.shape[0] * .26 + offset) 

    # Blur the region of interest (second top right corner box)
    blurred_roi_top_right2 = cv2.GaussianBlur(image[top_right_y:bottom_right_y, top_right_x:bottom_right_x], kernel_size, 0)
    # Create a copy of the original image
    output = image.copy()

    # Add the blurred region to the top middle 
    output[top_mid1_y:bottom_mid1_y, top_mid1_x:bottom_mid1_x] = blurred_roi_top_middle

    # Add the blurred region to the top right corner
    output[top_right3_y:bottom_right3_y, top_right3_x:bottom_right3_x] = blurred_roi_top_right

    # Add the blurred region to the top right corner
    output[top_right_y:bottom_right_y, top_right_x:bottom_right_x] = blurred_roi_top_right2
    
    # Save the output image
    cv2.imwrite(path, output) # Can be modified to not output photo
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

        case 'NB_02':
            blurNB_02(path)

        case _:
            return

## Code uses modification from posts found here: https://stackoverflow.com/questions/55066764/how-to-blur-feather-the-edges-of-an-object-in-an-image-using-opencv and https://forum.opencv.org/t/about-the-face-blurring-process/5008