import cv2 as cv
import pytesseract as pt

pt.pytesseract.tesseract_cmd = 'Car_Num_Plate_Detection\\pytessereact\\tesseract.exe'

img = cv.imread('Car_Plate_Detect\\4.png')
# img = cv.imread('Car_Num_Plate_Detection\\Data\\Pictures\\004.png')
img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
text = pt.image_to_string(image=img_rgb)
print(text)